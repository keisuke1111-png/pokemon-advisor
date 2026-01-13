'use client';

import { useMemo, useState } from 'react';
import type { Pokemon, PokemonType, Stats } from '@/lib/pokemon';
import { POKEMON_LIST } from '@/lib/pokemon';

const ALL_TYPES: PokemonType[] = [
  'ノーマル',
  'ほのお',
  'みず',
  'でんき',
  'くさ',
  'こおり',
  'かくとう',
  'どく',
  'じめん',
  'ひこう',
  'エスパー',
  'むし',
  'いわ',
  'ゴースト',
  'ドラゴン',
  'あく',
  'はがね',
  'フェアリー',
];

const STAT_LABELS: Record<keyof Stats, string> = {
  hp: 'H',
  atk: 'A',
  def: 'B',
  spa: 'C',
  spd: 'D',
  spe: 'S',
};

const STAT_KEYS = Object.keys(STAT_LABELS) as (keyof Stats)[];
const STAT_MIN = 40;
const STAT_MAX = 200;

const createInitialMinStats = () =>
  STAT_KEYS.reduce(
    (acc, key) => ({
      ...acc,
      [key]: STAT_MIN,
    }),
    {} as Record<keyof Stats, number>
  );

const sumStats = (stats: Stats) =>
  STAT_KEYS.reduce((total, key) => total + stats[key], 0);

const formatTypes = (types: Pokemon['types']) => types.join(' / ');

export default function Home() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTypes, setSelectedTypes] = useState<PokemonType[]>([]);
  const [minStats, setMinStats] = useState(createInitialMinStats);

  const filteredPokemon = useMemo(() => {
    const normalizedTerm = searchTerm.trim().toLowerCase();

    return POKEMON_LIST.filter((pokemon) => {
      const matchesText =
        normalizedTerm.length === 0 ||
        [pokemon.name, ...pokemon.abilities, ...pokemon.moves].some((entry) =>
          entry.toLowerCase().includes(normalizedTerm)
        );

      const matchesTypes =
        selectedTypes.length === 0 ||
        selectedTypes.every((type) => pokemon.types.includes(type));

      const matchesStats = STAT_KEYS.every(
        (key) => pokemon.stats[key] >= minStats[key]
      );

      return matchesText && matchesTypes && matchesStats;
    });
  }, [searchTerm, selectedTypes, minStats]);

  const toggleType = (type: PokemonType) => {
    setSelectedTypes((prev) =>
      prev.includes(type) ? prev.filter((t) => t !== type) : [...prev, type]
    );
  };

  const updateMinStat = (key: keyof Stats, value: number) => {
    const nextValue = Math.min(Math.max(value, STAT_MIN), STAT_MAX);
    setMinStats((prev) => ({ ...prev, [key]: nextValue }));
  };

  const resetFilters = () => {
    setSearchTerm('');
    setSelectedTypes([]);
    setMinStats(createInitialMinStats());
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <header className="space-y-3">
          <p className="text-xs uppercase tracking-[0.35em] text-emerald-300">
            Pokedex Intelligence
          </p>
          <h1 className="text-3xl font-semibold text-white md:text-4xl">
            ポケモン大図鑑 高性能検索エンジン
          </h1>
          <p className="max-w-2xl text-sm text-slate-300">
            種族値・タイプ・特性・技を同時にAND検索し、リアルタイムで結果を更新します。
          </p>
        </header>

        <div className="mt-10 flex flex-col gap-8 lg:flex-row">
          <aside className="w-full rounded-3xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg shadow-slate-950/40 lg:w-96">
            <div className="space-y-6">
              <div>
                <label className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
                  Search
                </label>
                <input
                  value={searchTerm}
                  onChange={(event) => setSearchTerm(event.target.value)}
                  placeholder="名前 / 技 / 特性を入力"
                  className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/70 px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-emerald-400 focus:outline-none"
                />
              </div>

              <div>
                <div className="flex items-center justify-between">
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
                    Types
                  </p>
                  <p className="text-xs text-slate-500">複合タイプ検索</p>
                </div>
                <div className="mt-3 flex flex-wrap gap-2">
                  {ALL_TYPES.map((type) => {
                    const active = selectedTypes.includes(type);
                    return (
                      <button
                        key={type}
                        type="button"
                        onClick={() => toggleType(type)}
                        aria-pressed={active}
                        className={`rounded-full border px-3 py-1 text-xs font-semibold transition ${
                          active
                            ? 'border-emerald-400 bg-emerald-400/20 text-emerald-200'
                            : 'border-slate-700 bg-slate-950/60 text-slate-300 hover:border-slate-500'
                        }`}
                      >
                        {type}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
                  Base Stats (Min)
                </p>
                <div className="mt-4 space-y-4">
                  {STAT_KEYS.map((key) => (
                    <div
                      key={key}
                      className="rounded-2xl border border-slate-800 bg-slate-950/40 p-4"
                    >
                      <div className="flex items-center justify-between text-xs text-slate-300">
                        <span className="font-semibold">{STAT_LABELS[key]}</span>
                        <span className="text-slate-400">{minStats[key]}+</span>
                      </div>
                      <input
                        type="range"
                        min={STAT_MIN}
                        max={STAT_MAX}
                        value={minStats[key]}
                        onChange={(event) =>
                          updateMinStat(key, Number(event.target.value))
                        }
                        className="mt-3 w-full accent-emerald-400"
                      />
                    </div>
                  ))}
                </div>
              </div>

              <div className="flex items-center justify-between">
                <p className="text-sm text-slate-400">
                  検索結果: <span className="text-white">{filteredPokemon.length}</span>匹
                </p>
                <button
                  type="button"
                  onClick={resetFilters}
                  className="rounded-full border border-slate-700 px-4 py-2 text-xs font-semibold text-slate-200 transition hover:border-emerald-400 hover:text-emerald-200"
                >
                  リセット
                </button>
              </div>
            </div>
          </aside>

          <section className="flex-1">
            <div className="grid gap-6 md:grid-cols-2">
              {filteredPokemon.map((pokemon) => {
                const bst = sumStats(pokemon.stats);
                return (
                  <article
                    key={pokemon.id}
                    className="rounded-3xl border border-slate-800 bg-gradient-to-br from-slate-900/80 via-slate-950 to-slate-900/60 p-6 shadow-lg shadow-slate-950/40"
                  >
                    <header className="flex items-start justify-between">
                      <div>
                        <p className="text-xs uppercase tracking-[0.3em] text-slate-500">
                          #{pokemon.id}
                        </p>
                        <h2 className="mt-2 text-2xl font-semibold text-white">
                          {pokemon.name}
                        </h2>
                        <p className="mt-1 text-xs text-emerald-200">
                          {formatTypes(pokemon.types)}
                        </p>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {pokemon.types.map((type) => (
                          <span
                            key={`${pokemon.id}-${type}`}
                            className="rounded-full border border-emerald-400/40 bg-emerald-400/10 px-3 py-1 text-[11px] font-semibold text-emerald-200"
                          >
                            {type}
                          </span>
                        ))}
                      </div>
                    </header>

                    <div className="mt-4 flex items-center justify-between text-xs text-slate-400">
                      <span>BST</span>
                      <span className="text-base font-semibold text-white">{bst}</span>
                    </div>

                    <div className="mt-4 space-y-3">
                      {STAT_KEYS.map((key) => {
                        const value = pokemon.stats[key];
                        const width = Math.round((value / STAT_MAX) * 100);
                        return (
                          <div key={`${pokemon.id}-${key}`} className="space-y-1">
                            <div className="flex items-center justify-between text-xs text-slate-400">
                              <span>{STAT_LABELS[key]}</span>
                              <span className="text-slate-200">{value}</span>
                            </div>
                            <div className="h-2 rounded-full bg-slate-800">
                              <div
                                className="h-2 rounded-full bg-emerald-400"
                                style={{ width: `${width}%` }}
                              />
                            </div>
                          </div>
                        );
                      })}
                    </div>

                    <div className="mt-5 grid gap-3 text-xs text-slate-300">
                      <div>
                        <p className="text-[10px] uppercase tracking-[0.2em] text-slate-500">
                          Abilities
                        </p>
                        <p className="mt-1 text-sm text-slate-200">
                          {pokemon.abilities.join(' / ')}
                        </p>
                      </div>
                      <div>
                        <p className="text-[10px] uppercase tracking-[0.2em] text-slate-500">
                          Moves
                        </p>
                        <p className="mt-1 text-sm text-slate-200">
                          {pokemon.moves.join(' / ')}
                        </p>
                      </div>
                    </div>
                  </article>
                );
              })}
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}
