'use client';

import { CacheProvider } from '@chakra-ui/next-js';
import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import { SessionProvider } from 'next-auth/react';

// Tema personalizado do Chakra UI
const theme = extendTheme({
  colors: {
    brand: {
      50: '#f0e4ff',
      100: '#d1beff',
      200: '#b397ff',
      300: '#9470ff',
      400: '#7549ff',
      500: '#5622ff',
      600: '#4805ff',
      700: '#3a04cc',
      800: '#2c0399',
      900: '#1e0266',
    },
  },
  fonts: {
    heading: `'Inter', sans-serif`,
    body: `'Inter', sans-serif`,
  },
  styles: {
    global: {
      body: {
        bg: 'gray.50',
        color: 'gray.800',
      },
    },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <SessionProvider>
      <CacheProvider>
        <ChakraProvider theme={theme}>
          {children}
        </ChakraProvider>
      </CacheProvider>
    </SessionProvider>
  );
} 