import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { ChakraProvider } from '@chakra-ui/react';
import { Providers } from './providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'CodeSpark - Desenvolva projetos guiados por IA',
  description: 'Plataforma para criação de projetos personalizados guiados por IA',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
} 