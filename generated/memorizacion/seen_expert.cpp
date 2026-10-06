// Tasa de prefijos vistos por jugada, con la política del experto (rho=0.3, P=0).
// Reimplementación en C++ de seen_expert.py, enlazando el solver de Pons en proceso.
//
// Compilar (desde generated/memorizacion):
//   g++ -std=c++17 -O3 -DNDEBUG -pthread -I../../solver/third_party/connect4 \
//       seen_expert.cpp ../../solver/third_party/connect4/Solver.cpp -o seen_expert
// Correr:  ./seen_expert <n_train> <n_test> [workers] [semilla_base]
#include "Solver.hpp"
#include "Position.hpp"

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <random>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>
#include <cstdlib>
#ifdef __APPLE__
#include <pthread.h>
#include <sys/qos.h>
#endif

using namespace GameSolver::Connect4;

static const double RHO = 0.3;
static const int W = Position::WIDTH, H = Position::HEIGHT;
static const std::string BOOK = "../../solver/third_party/connect4/7x6.book";

struct Game {
  std::string moves;         // columnas '1'..'7'
  uint64_t nontrivial = 0;   // bit t = el estado antes de la jugada t+1 es no trivial
};

// Un solver + caché por hilo (como el wrapper de Python: no se comparte entre workers).
struct Expert {
  Solver solver;
  std::unordered_map<Position::position_t, std::array<int8_t, 7>> cache;
  std::mt19937_64 rng;
  std::uniform_real_distribution<double> unif{0.0, 1.0};

  Expert(uint64_t seed) : rng(seed) {
    solver.loadBook(BOOK);
    cache.reserve(1 << 20);
  }

  // Resultado (para quien mueve) de cada columna: +1 gana, 0 empata, -1 pierde, -100 ilegal.
  const std::array<int8_t, 7>& outcomes(const Position& P) {
    auto it = cache.find(P.key());
    if (it != cache.end()) return it->second;
    std::vector<int> s = solver.analyze(P, /*weak=*/true);
    std::array<int8_t, 7> o;
    for (int c = 0; c < W; c++)
      o[c] = s[c] == Solver::INVALID_MOVE ? -100 : (s[c] > 0 ? 1 : (s[c] < 0 ? -1 : 0));
    if (cache.size() >= 2'000'000) cache.clear();
    return cache.emplace(P.key(), o).first->second;
  }

  int pick(const std::vector<int>& v) {
    return v[std::uniform_int_distribution<size_t>(0, v.size() - 1)(rng)];
  }

  Game play() {
    Position P;
    Game g;
    bool over = false;
    while (!over && P.nbMoves() < W * H) {
      const auto& o = outcomes(P);
      int8_t best = -100;
      for (int c = 0; c < W; c++) if (o[c] != -100) best = std::max(best, o[c]);
      std::vector<int> opt, wrong;
      for (int c = 0; c < W; c++) {
        if (o[c] == -100) continue;
        (o[c] == best ? opt : wrong).push_back(c);
      }
      bool nt = !wrong.empty();
      int c;
      if (!nt) c = pick(opt);
      else if (unif(rng) < RHO) c = pick(wrong);
      else c = pick(opt);
      if (nt) g.nontrivial |= (1ULL << P.nbMoves());
      if (P.isWinningMove(c)) over = true;
      P.playCol(c);
      g.moves.push_back(char('1' + c));
    }
    return g;
  }
};

static std::vector<Game> generate(size_t n, uint64_t seed, int workers) {
  std::vector<std::vector<Game>> chunks(workers);
  std::vector<std::thread> threads;
  for (int i = 0; i < workers; i++)
    threads.emplace_back([&, i] {
#ifdef __APPLE__
      // Sin esto macOS manda los threads a los efficiency cores: 781s vs 421s para 80K partidas.
      pthread_set_qos_class_self_np(QOS_CLASS_USER_INTERACTIVE, 0);
#endif
      Expert e(seed * 1000 + i);
      chunks[i].reserve(n / workers);
      for (size_t k = 0; k < n / workers; k++) chunks[i].push_back(e.play());
    });
  for (auto& t : threads) t.join();
  std::vector<Game> all;
  all.reserve(n);
  for (auto& ch : chunks) for (auto& g : ch) all.push_back(std::move(g));
  return all;
}

static inline uint64_t pkey(const std::string& m, size_t t) {
  return std::hash<std::string_view>{}(std::string_view(m.data(), t));
}

int main(int argc, char** argv) {
  size_t n_train = std::stoul(argv[1]), n_test = std::stoul(argv[2]);
  int workers = argc > 3 ? std::stoi(argv[3]) : 10;
  uint64_t base = argc > 4 ? std::stoul(argv[4]) : 0;  // desplaza las semillas (para correr varios procesos)
  auto t0 = std::chrono::steady_clock::now();
  auto train = generate(n_train, 1 + base, workers);
  auto test = generate(n_test, 2 + base, workers);
  auto t1 = std::chrono::steady_clock::now();
  std::printf("generadas %zu+%zu partidas en %.0fs\n", train.size(), test.size(),
              std::chrono::duration<double>(t1 - t0).count());
  std::fflush(stdout);

  std::unordered_map<uint64_t, uint32_t> cnt;
  cnt.reserve(train.size() * 22);
  for (const auto& g : train)
    for (size_t t = 0; t <= g.moves.size(); t++) cnt[pkey(g.moves, t)]++;
  auto visits = [&](const std::string& m, size_t t) {
    auto it = cnt.find(pkey(m, t));
    return it == cnt.end() ? 0u : it->second;
  };

  std::printf("N_train=%zu: por jugada t (estado ANTES de la jugada t+1 => prefijo de largo t)\n", n_train);
  std::printf(" t | %%test vistos | %%test NO-triv vistos | mediana visitas (vistos) | n test\n");
  size_t tot_nt = 0, seen_nt = 0;
  for (size_t t = 0; t < 42; t++) {
    size_t n = 0, seen = 0, n_nt = 0, seen_nt_t = 0;
    std::vector<uint32_t> sv;
    for (const auto& g : test) {
      if (g.moves.size() <= t) continue;
      uint32_t v = visits(g.moves, t);
      bool nt = (g.nontrivial >> t) & 1;
      n++; if (v) { seen++; sv.push_back(v); }
      if (nt) { n_nt++; if (v) seen_nt_t++; }
    }
    if (!n) break;
    tot_nt += n_nt; seen_nt += seen_nt_t;
    std::sort(sv.begin(), sv.end());
    uint32_t med = sv.empty() ? 0 : sv[sv.size() / 2];
    std::printf("%2zu | %5.0f%% | %5.0f%% (%5zu) | %8u | %zu\n", t, 100.0 * seen / n,
                100.0 * seen_nt_t / std::max<size_t>(1, n_nt), n_nt, med, n);
  }
  std::printf("fraccion de estados no triviales de test vistos en train: %.1f%%\n", 100.0 * seen_nt / tot_nt);
  std::vector<uint32_t> nt_all;
  for (const auto& g : test)
    for (size_t t = 0; t < g.moves.size(); t++)
      if ((g.nontrivial >> t) & 1) nt_all.push_back(visits(g.moves, t));
  for (uint32_t th : {1u, 10u, 100u}) {
    size_t k = std::count_if(nt_all.begin(), nt_all.end(), [&](uint32_t v) { return v >= th; });
    std::printf("no triviales de test con >= %u visitas en train: %.1f%%\n", th, 100.0 * k / nt_all.size());
  }
  auto t2 = std::chrono::steady_clock::now();
  std::printf("tiempo total: %.0fs (generacion %.0fs, analisis %.0fs)\n",
              std::chrono::duration<double>(t2 - t0).count(),
              std::chrono::duration<double>(t1 - t0).count(),
              std::chrono::duration<double>(t2 - t1).count());
}
