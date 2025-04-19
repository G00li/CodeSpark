'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  Box,
  Button,
  Container,
  FormControl,
  FormLabel,
  Heading,
  Input,
  Select,
  Text,
  VStack,
  HStack,
  Tag,
  TagLabel,
  TagCloseButton,
  Textarea,
  useToast,
  Card,
  CardBody,
  CardHeader,
  Divider,
  List,
  ListItem,
  ListIcon,
  Spinner,
  Flex,
} from '@chakra-ui/react';
import { FiCheckCircle } from 'react-icons/fi';
import axios from 'axios';

type ProjectType = 'frontend' | 'backend' | 'fullstack';
type ProjectTask = {
  title: string;
  description: string;
};

type ProjectProposal = {
  title: string;
  description: string;
  goals: string[];
  tasks: ProjectTask[];
  technologies: string[];
};

export default function CreateProject() {
  const router = useRouter();
  const toast = useToast();
  
  // Estados para o formulário
  const [projectType, setProjectType] = useState<ProjectType>('frontend');
  const [technology, setTechnology] = useState<string>('');
  const [technologies, setTechnologies] = useState<string[]>([]);
  const [additionalInfo, setAdditionalInfo] = useState<string>('');
  
  // Estado para proposta gerada
  const [proposal, setProposal] = useState<ProjectProposal | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  
  // Adicionar tecnologia à lista
  const addTechnology = () => {
    if (technology.trim() && !technologies.includes(technology.trim())) {
      setTechnologies([...technologies, technology.trim()]);
      setTechnology('');
    }
  };
  
  // Remover tecnologia da lista
  const removeTechnology = (tech: string) => {
    setTechnologies(technologies.filter(t => t !== tech));
  };
  
  // Gerar proposta de projeto
  const generateProjectProposal = async () => {
    if (technologies.length === 0) {
      toast({
        title: 'Selecione pelo menos uma tecnologia',
        status: 'warning',
        duration: 3000,
        isClosable: true,
      });
      return;
    }
    
    setIsLoading(true);
    
    try {
      // Na implementação real, esta seria uma chamada para a API backend
      // Exemplo: const response = await axios.post('/api/generate-project', { ... });
      
      // Simulação de resposta para demonstração
      setTimeout(() => {
        const mockProposal: ProjectProposal = {
          title: `Projeto ${projectType === 'frontend' ? 'de Interface' : projectType === 'backend' ? 'de API' : 'Fullstack'} com ${technologies[0]}`,
          description: `Este projeto foi criado para ajudar no aprendizado e prática de ${technologies.join(', ')}. O objetivo é criar uma aplicação completa seguindo boas práticas de desenvolvimento.`,
          goals: [
            'Desenvolver um projeto do início ao fim',
            'Praticar o uso das tecnologias selecionadas',
            'Seguir boas práticas de desenvolvimento',
            'Criar uma aplicação funcional e escalável'
          ],
          tasks: [
            {
              title: 'Configuração inicial do ambiente',
              description: 'Configurar o ambiente de desenvolvimento com todas as dependências necessárias.'
            },
            {
              title: 'Estrutura básica do projeto',
              description: 'Criar a estrutura básica do projeto seguindo as melhores práticas.'
            },
            {
              title: 'Implementação das principais funcionalidades',
              description: 'Desenvolver as funcionalidades principais da aplicação.'
            },
            {
              title: 'Testes e validação',
              description: 'Criar testes para garantir o funcionamento correto da aplicação.'
            },
            {
              title: 'Documentação e finalização',
              description: 'Documentar o projeto e finalizar para implantação.'
            }
          ],
          technologies: technologies
        };
        
        setProposal(mockProposal);
        setIsLoading(false);
      }, 2000);
    } catch (error) {
      console.error('Erro ao gerar proposta:', error);
      toast({
        title: 'Erro ao gerar proposta de projeto',
        description: 'Ocorreu um erro ao comunicar com o serviço de IA. Tente novamente mais tarde.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      setIsLoading(false);
    }
  };
  
  // Criar o projeto a partir da proposta
  const createProject = async () => {
    if (!proposal) return;
    
    try {
      // Na implementação real, esta seria uma chamada para a API backend
      // const response = await axios.post('/api/projects', { 
      //   title: proposal.title,
      //   description: proposal.description,
      //   project_type: projectType,
      //   technologies: technologies.join(', ')
      // });
      
      toast({
        title: 'Projeto criado com sucesso!',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      
      // Redirecionar para a página do projeto
      router.push('/dashboard');
    } catch (error) {
      console.error('Erro ao criar projeto:', error);
      toast({
        title: 'Erro ao criar projeto',
        description: 'Ocorreu um erro ao salvar o projeto. Tente novamente mais tarde.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };
  
  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={8} align="stretch">
        <Heading size="lg">Criar Novo Projeto</Heading>
        
        <Box>
          {!proposal ? (
            <Card boxShadow="md">
              <CardHeader>
                <Heading size="md">Defina seu projeto</Heading>
              </CardHeader>
              <Divider />
              <CardBody>
                <VStack spacing={6} align="stretch">
                  <FormControl>
                    <FormLabel>Tipo de Projeto</FormLabel>
                    <Select
                      value={projectType}
                      onChange={(e) => setProjectType(e.target.value as ProjectType)}
                    >
                      <option value="frontend">Frontend</option>
                      <option value="backend">Backend</option>
                      <option value="fullstack">Fullstack</option>
                    </Select>
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Tecnologias</FormLabel>
                    <HStack>
                      <Input
                        placeholder="Ex: React, Node.js, MongoDB..."
                        value={technology}
                        onChange={(e) => setTechnology(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && addTechnology()}
                      />
                      <Button onClick={addTechnology} colorScheme="brand">
                        Adicionar
                      </Button>
                    </HStack>
                    
                    <Box mt={4}>
                      <HStack spacing={2} flexWrap="wrap">
                        {technologies.map((tech) => (
                          <Tag
                            key={tech}
                            borderRadius="full"
                            variant="solid"
                            colorScheme="brand"
                            size="md"
                            m={1}
                          >
                            <TagLabel>{tech}</TagLabel>
                            <TagCloseButton onClick={() => removeTechnology(tech)} />
                          </Tag>
                        ))}
                      </HStack>
                    </Box>
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Informações Adicionais (opcional)</FormLabel>
                    <Textarea
                      placeholder="Descreva qualquer outra informação relevante para o seu projeto..."
                      value={additionalInfo}
                      onChange={(e) => setAdditionalInfo(e.target.value)}
                    />
                  </FormControl>
                  
                  <Button
                    colorScheme="brand"
                    size="lg"
                    onClick={generateProjectProposal}
                    isLoading={isLoading}
                    loadingText="Gerando proposta..."
                    isDisabled={technologies.length === 0}
                  >
                    Gerar Proposta de Projeto
                  </Button>
                </VStack>
              </CardBody>
            </Card>
          ) : (
            <Card boxShadow="md">
              <CardHeader>
                <Heading size="md">Proposta de Projeto</Heading>
              </CardHeader>
              <Divider />
              <CardBody>
                <VStack spacing={6} align="stretch">
                  <Box>
                    <Heading size="lg" color="brand.600">
                      {proposal.title}
                    </Heading>
                    <Text mt={2} fontSize="md">
                      {proposal.description}
                    </Text>
                  </Box>
                  
                  <Box>
                    <Heading size="sm" mb={2}>
                      Objetivos
                    </Heading>
                    <List spacing={2}>
                      {proposal.goals.map((goal, index) => (
                        <ListItem key={index} display="flex">
                          <ListIcon as={FiCheckCircle} color="brand.500" mt={1} />
                          <Text>{goal}</Text>
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                  
                  <Box>
                    <Heading size="sm" mb={2}>
                      Tarefas
                    </Heading>
                    <VStack spacing={4} align="stretch">
                      {proposal.tasks.map((task, index) => (
                        <Box
                          key={index}
                          p={4}
                          borderRadius="md"
                          bg="gray.50"
                          borderLeft="4px solid"
                          borderColor="brand.500"
                        >
                          <Heading size="xs" mb={1}>
                            {index + 1}. {task.title}
                          </Heading>
                          <Text fontSize="sm">{task.description}</Text>
                        </Box>
                      ))}
                    </VStack>
                  </Box>
                  
                  <Box>
                    <Heading size="sm" mb={2}>
                      Tecnologias
                    </Heading>
                    <HStack spacing={2} flexWrap="wrap">
                      {proposal.technologies.map((tech) => (
                        <Tag
                          key={tech}
                          borderRadius="full"
                          variant="solid"
                          colorScheme="brand"
                          size="md"
                          m={1}
                        >
                          <TagLabel>{tech}</TagLabel>
                        </Tag>
                      ))}
                    </HStack>
                  </Box>
                  
                  <Flex justify="space-between" mt={4}>
                    <Button
                      variant="outline"
                      onClick={() => setProposal(null)}
                    >
                      Voltar
                    </Button>
                    
                    <Button
                      colorScheme="brand"
                      size="lg"
                      onClick={createProject}
                    >
                      Aceitar e Criar Projeto
                    </Button>
                  </Flex>
                </VStack>
              </CardBody>
            </Card>
          )}
        </Box>
      </VStack>
    </Container>
  );
} 