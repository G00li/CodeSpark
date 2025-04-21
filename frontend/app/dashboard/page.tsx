'use client';

import { useEffect, useState } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import {
  Box,
  Container,
  Heading,
  Text,
  Button,
  Flex,
  Grid,
  GridItem,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Badge,
  VStack,
  Icon,
  Divider,
  useToast,
} from '@chakra-ui/react';
import { FiPlus, FiCode, FiServer, FiLayers } from 'react-icons/fi';

import axios from 'axios';
import api from '@/services/api';

// Tipos
type Project = {
  id: number;
  title: string;
  description: string;
  project_type: 'frontend' | 'backend' | 'fullstack';
  technologies: string;
  created_at: string;
};

export default function Dashboard() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const toast = useToast();
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Redireciona para login se não estiver autenticado
  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/login');
    }
  }, [status, router]);

  // Carrega os projetos do usuário
  useEffect(() => {
    if (session?.user) {
      const fetchProjects = async () => {
        try {
          // Usar o id do usuário da sessão ou um valor padrão para teste
          const userId = session.user.id || '1';
          
          // Tentar obter projetos do backend
          const response = await api.get(`/api/projects/user/${userId}`);
          
          if (response.data && response.data.length > 0) {
            setProjects(response.data);
          } else {
            // Se não houver projetos, carregar dados de exemplo
            setProjects(getDemoProjects());
          }
        } catch (error) {
          console.error('Erro ao carregar projetos:', error);
          toast({
            title: 'Erro ao carregar projetos',
            description: 'Usando dados de demonstração',
            status: 'warning',
            duration: 3000,
            isClosable: true,
          });
          
          // Carregar dados de exemplo em caso de erro
          setProjects(getDemoProjects());
        } finally {
          setIsLoading(false);
        }
      };

      fetchProjects();
    }
  }, [session, toast]);

  // Função para retornar projetos de demonstração
  const getDemoProjects = (): Project[] => {
    return [
      {
        id: 1,
        title: 'Sistema de Blog com React',
        description: 'Um blog completo com autenticação e painel de administração.',
        project_type: 'frontend',
        technologies: 'React, Redux, TailwindCSS',
        created_at: '2023-12-01',
      },
      {
        id: 2,
        title: 'API REST para E-commerce',
        description: 'API para um sistema de e-commerce com autenticação, produtos e pedidos.',
        project_type: 'backend',
        technologies: 'Node.js, Express, MongoDB',
        created_at: '2023-12-10',
      },
    ];
  };

  const getProjectTypeIcon = (type: string) => {
    switch (type) {
      case 'frontend':
        return FiCode;
      case 'backend':
        return FiServer;
      case 'fullstack':
        return FiLayers;
      default:
        return FiCode;
    }
  };

  const getProjectTypeBadge = (type: string) => {
    switch (type) {
      case 'frontend':
        return { colorScheme: 'blue', text: 'Frontend' };
      case 'backend':
        return { colorScheme: 'green', text: 'Backend' };
      case 'fullstack':
        return { colorScheme: 'purple', text: 'Fullstack' };
      default:
        return { colorScheme: 'gray', text: type };
    }
  };

  return (
    <Container maxW="container.xl" py={8}>
      <Flex justifyContent="space-between" alignItems="center" mb={8}>
        <Heading size="lg">Meus Projetos</Heading>
        
        <Button 
          leftIcon={<FiPlus />} 
          colorScheme="brand" 
          onClick={() => router.push('/create-project')}
        >
          Novo Projeto
        </Button>
      </Flex>

      <Grid templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' }} gap={6}>
        {projects.map((project) => (
          <GridItem key={project.id}>
            <Card 
              h="100%" 
              boxShadow="md" 
              borderRadius="lg" 
              cursor="pointer" 
              transition="transform 0.2s"
              _hover={{ transform: 'translateY(-5px)', boxShadow: 'lg' }}
              onClick={() => router.push(`/project/${project.id}`)}
            >
              <CardHeader pb={0}>
                <Flex justify="space-between" align="flex-start">
                  <Heading size="md" color="brand.600" noOfLines={2}>
                    {project.title}
                  </Heading>
                  <Icon 
                    as={getProjectTypeIcon(project.project_type)} 
                    boxSize={6} 
                    color="brand.500" 
                  />
                </Flex>
              </CardHeader>
              
              <CardBody>
                <Text fontSize="sm" color="gray.600" noOfLines={3}>
                  {project.description}
                </Text>
                
                <Box mt={4}>
                  <Badge {...getProjectTypeBadge(project.project_type)}>
                    {getProjectTypeBadge(project.project_type).text}
                  </Badge>
                </Box>
              </CardBody>
              
              <CardFooter pt={0}>
                <VStack align="start" spacing={2} w="full">
                  <Divider />
                  <Text fontSize="xs" color="gray.500">
                    Tecnologias: {project.technologies}
                  </Text>
                  <Text fontSize="xs" color="gray.500">
                    Criado em: {new Date(project.created_at).toLocaleDateString('pt-BR')}
                  </Text>
                </VStack>
              </CardFooter>
            </Card>
          </GridItem>
        ))}
        
        {/* Card para criar novo projeto */}
        <GridItem>
          <Card
            h="100%"
            boxShadow="md"
            borderRadius="lg"
            cursor="pointer"
            transition="transform 0.2s"
            _hover={{ transform: 'translateY(-5px)', boxShadow: 'lg' }}
            onClick={() => router.push('/create-project')}
            bg="gray.50"
            borderStyle="dashed"
            borderWidth={2}
            borderColor="gray.200"
          >
            <CardBody>
              <VStack justify="center" align="center" h="100%" spacing={4} py={10}>
                <Icon as={FiPlus} boxSize={10} color="gray.400" />
                <Text color="gray.500" fontWeight="medium">
                  Criar Novo Projeto
                </Text>
              </VStack>
            </CardBody>
          </Card>
        </GridItem>
      </Grid>
    </Container>
  );
} 