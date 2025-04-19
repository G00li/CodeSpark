'use client';

import { Box, Button, Container, Flex, Heading, Text, VStack, Image, useColorModeValue } from '@chakra-ui/react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useEffect, useState } from 'react';

export default function Home() {
  const { data: session } = useSession();
  const router = useRouter();
  const bgGradient = 'linear(to-r, brand.500, purple.500)';
  const buttonBg = useColorModeValue('brand.500', 'brand.400');
  
  const [apiUrl, setApiUrl] = useState<string>('');
  
  useEffect(() => {
    setApiUrl(process.env.NEXT_PUBLIC_API_URL || 'Não definido');
  }, []);

  return (
    <Box>
      <Container maxW="container.xl" py={10}>
        <Box 
          p={4} 
          mb={4} 
          bg="gray.100" 
          borderRadius="md"
          border="1px solid"
          borderColor="gray.300"
          display="block"
        >
          <Heading size="xs" mb={2}>Informações de Debug</Heading>
          <Text fontSize="sm">API URL: {apiUrl}</Text>
        </Box>
        
        <Flex
          direction={{ base: 'column', md: 'row' }}
          align="center"
          justify="space-between"
          py={20}
          gap={10}
        >
          <VStack align="flex-start" spacing={6} maxW={{ base: 'full', md: '50%' }}>
            <Heading
              as="h1"
              size="3xl"
              bgGradient={bgGradient}
              bgClip="text"
              lineHeight="1.2"
            >
              Aprenda programação construindo projetos reais
            </Heading>
            <Text fontSize="xl" color="gray.600">
              O CodeSpark usa IA para criar trilhas de aprendizado personalizadas
              com base nas tecnologias que você deseja dominar.
            </Text>
            <Flex gap={4} pt={4}>
              {session ? (
                <Button
                  size="lg"
                  bg={buttonBg}
                  color="white"
                  _hover={{ bg: 'brand.600' }}
                  onClick={() => router.push('/dashboard')}
                >
                  Meus Projetos
                </Button>
              ) : (
                <Button
                  size="lg"
                  bg={buttonBg}
                  color="white"
                  _hover={{ bg: 'brand.600' }}
                  onClick={() => router.push('/login')}
                >
                  Começar Agora
                </Button>
              )}
              <Button
                size="lg"
                variant="outline"
                borderColor="brand.500"
                color="brand.500"
                _hover={{ bg: 'brand.50' }}
                onClick={() => router.push('/about')}
              >
                Saiba Mais
              </Button>
            </Flex>
          </VStack>
          
          <Box maxW={{ base: 'full', md: '45%' }}>
            <Image
              src="/images/hero-image.svg"
              alt="CodeSpark illustration"
              fallbackSrc="https://via.placeholder.com/500x400?text=CodeSpark"
            />
          </Box>
        </Flex>

        <Box py={20}>
          <VStack spacing={16}>
            <Heading
              textAlign="center"
              bgGradient={bgGradient}
              bgClip="text"
              size="xl"
            >
              Como funciona
            </Heading>
            
            <Flex
              wrap="wrap"
              justify="space-between"
              gap={8}
            >
              <FeatureCard
                title="Selecione suas tecnologias"
                description="Escolha as tecnologias que deseja aprender ou praticar e o tipo de projeto que deseja desenvolver."
                number="1"
              />
              <FeatureCard
                title="Receba sua proposta"
                description="Nossa IA (CrewAI) irá gerar uma proposta de projeto desafiadora e realista com as tecnologias escolhidas."
                number="2"
              />
              <FeatureCard
                title="Siga sua trilha"
                description="Receba tarefas diárias e acompanhe seu progresso enquanto desenvolve um projeto completo."
                number="3"
              />
            </Flex>
          </VStack>
        </Box>
      </Container>
    </Box>
  );
}

function FeatureCard({ title, description, number }: { title: string; description: string; number: string }) {
  return (
    <Box 
      p={8} 
      boxShadow="lg" 
      borderRadius="xl" 
      bg="white" 
      flex="1" 
      minW={{ base: 'full', md: '30%' }}
      position="relative"
      overflow="hidden"
    >
      <Box
        position="absolute"
        top="-5"
        right="-5"
        fontSize="9xl"
        fontWeight="bold"
        opacity="0.1"
        color="brand.500"
      >
        {number}
      </Box>
      <VStack align="flex-start" spacing={4} zIndex="1" position="relative">
        <Heading size="md" color="brand.500">{title}</Heading>
        <Text color="gray.600">{description}</Text>
      </VStack>
    </Box>
  );
} 