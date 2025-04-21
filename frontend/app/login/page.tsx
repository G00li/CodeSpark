"use client";

import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";
import {
  Box,
  Button,
  VStack,
  Heading,
  Text,
  Container,
  Divider,
  useToast,
  Center,
  Icon,
} from "@chakra-ui/react";
import { FaGoogle, FaGithub } from "react-icons/fa";

export default function LoginPage() {
  const router = useRouter();
  const toast = useToast();

  const handleLogin = async (provider: string) => {
    try {
      const result = await signIn(provider, {
        callbackUrl: "/dashboard",
      });
      
      if (result?.error) {
        toast({
          title: "Erro de autenticação",
          description: `Não foi possível fazer login com ${provider}`,
          status: "error",
          duration: 5000,
          isClosable: true,
        });
      }
    } catch (error) {
      toast({
        title: "Erro",
        description: "Ocorreu um erro ao tentar fazer login",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Container maxW="md" py={12}>
      <VStack spacing={8}>
        <Heading>Login</Heading>
        <Box w="100%" p={8} borderWidth={1} borderRadius="lg">
          <VStack spacing={4}>
            <Text align="center" mb={4}>
              Faça login com sua conta:
            </Text>
            
            <Button
              w="full"
              colorScheme="red"
              leftIcon={<Icon as={FaGoogle} />}
              onClick={() => handleLogin("google")}
            >
              Continuar com Google
            </Button>
            
            <Button
              w="full"
              colorScheme="gray"
              leftIcon={<Icon as={FaGithub} />}
              onClick={() => handleLogin("github")}
            >
              Continuar com GitHub
            </Button>
            
            <Divider my={6} />
            
            <Text fontSize="sm" color="gray.500" textAlign="center">
              Ao fazer login, você concorda com os Termos de Serviço e Política de Privacidade.
            </Text>
          </VStack>
        </Box>
      </VStack>
    </Container>
  );
} 