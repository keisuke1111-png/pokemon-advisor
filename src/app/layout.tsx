import './globals.css';
import type { ReactNode } from 'react';

export const metadata = {
  title: 'ポケモン大図鑑',
  description: '種族値・タイプ・特性・技で絞り込む高性能検索エンジン',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
