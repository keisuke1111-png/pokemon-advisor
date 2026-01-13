export type PokemonType =
  | 'ノーマル'
  | 'ほのお'
  | 'みず'
  | 'でんき'
  | 'くさ'
  | 'こおり'
  | 'かくとう'
  | 'どく'
  | 'じめん'
  | 'ひこう'
  | 'エスパー'
  | 'むし'
  | 'いわ'
  | 'ゴースト'
  | 'ドラゴン'
  | 'あく'
  | 'はがね'
  | 'フェアリー';

export type Stats = {
  hp: number;
  atk: number;
  def: number;
  spa: number;
  spd: number;
  spe: number;
};

export type Pokemon = {
  id: number;
  name: string;
  types: [PokemonType] | [PokemonType, PokemonType];
  abilities: string[];
  moves: string[];
  stats: Stats;
};

export const POKEMON_LIST: Pokemon[] = [
  {
    id: 149,
    name: 'カイリュー',
    types: ['ドラゴン', 'ひこう'],
    abilities: ['マルチスケイル', 'せいしんりょく'],
    moves: ['しんそく', 'りゅうのまい', 'げきりん', 'じしん'],
    stats: { hp: 91, atk: 134, def: 95, spa: 100, spd: 100, spe: 80 },
  },
  {
    id: 987,
    name: 'ハバタクカミ',
    types: ['ゴースト', 'フェアリー'],
    abilities: ['こだいかっせい'],
    moves: ['ムーンフォース', 'シャドーボール', 'マジカルフレイム', 'みがわり'],
    stats: { hp: 55, atk: 55, def: 55, spa: 135, spd: 135, spe: 135 },
  },
  {
    id: 892,
    name: 'ウーラオス(れんげきのかた)',
    types: ['かくとう', 'みず'],
    abilities: ['ふかしのこぶし'],
    moves: ['すいりゅうれんだ', 'インファイト', 'アクアジェット', 'つるぎのまい'],
    stats: { hp: 100, atk: 130, def: 100, spa: 63, spd: 60, spe: 97 },
  },
  {
    id: 1002,
    name: 'パオジアン',
    types: ['あく', 'こおり'],
    abilities: ['わざわいのつるぎ'],
    moves: ['つららおとし', 'かみくだく', 'せいなるつるぎ', 'ふいうち'],
    stats: { hp: 80, atk: 120, def: 80, spa: 90, spd: 65, spe: 135 },
  },
  {
    id: 1000,
    name: 'サーフゴー',
    types: ['ゴースト', 'はがね'],
    abilities: ['おうごんのからだ'],
    moves: ['ゴールドラッシュ', 'シャドーボール', 'わるだくみ', 'きあいだま'],
    stats: { hp: 87, atk: 60, def: 95, spa: 133, spd: 91, spe: 84 },
  },
  {
    id: 645,
    name: 'ランドロス(れいじゅうフォルム)',
    types: ['じめん', 'ひこう'],
    abilities: ['いかく'],
    moves: ['じしん', 'とんぼがえり', 'ストーンエッジ', 'つるぎのまい'],
    stats: { hp: 89, atk: 145, def: 90, spa: 105, spd: 80, spe: 91 },
  },
  {
    id: 1003,
    name: 'ディンルー',
    types: ['あく', 'じめん'],
    abilities: ['わざわいのうつわ'],
    moves: ['じしん', 'まきびし', 'ステルスロック', 'じわれ'],
    stats: { hp: 155, atk: 110, def: 125, spa: 45, spd: 80, spe: 50 },
  },
  {
    id: 991,
    name: 'テツノツツミ',
    types: ['こおり', 'みず'],
    abilities: ['クォークチャージ'],
    moves: ['フリーズドライ', 'ハイドロポンプ', 'こおりのつぶて', 'みがわり'],
    stats: { hp: 56, atk: 80, def: 114, spa: 124, spd: 60, spe: 136 },
  },
  {
    id: 445,
    name: 'ガブリアス',
    types: ['ドラゴン', 'じめん'],
    abilities: ['すながくれ', 'さめはだ'],
    moves: ['じしん', 'げきりん', 'アイアンヘッド', 'ほのおのキバ'],
    stats: { hp: 108, atk: 130, def: 95, spa: 80, spd: 85, spe: 102 },
  },
  {
    id: 1004,
    name: 'イーユイ',
    types: ['あく', 'ほのお'],
    abilities: ['わざわいのたま'],
    moves: ['かえんほうしゃ', 'あくのはどう', 'おにび', 'わるだくみ'],
    stats: { hp: 55, atk: 80, def: 80, spa: 135, spd: 120, spe: 100 },
  },
];
