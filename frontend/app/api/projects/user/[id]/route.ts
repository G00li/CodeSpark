import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const userId = params.id;
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    // Obter token de autenticação da requisição
    const authHeader = request.headers.get('authorization');
    
    // Fazer a requisição para o backend
    const response = await fetch(`${apiUrl}/api/projects/user/${userId}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(authHeader ? { 'Authorization': authHeader } : {}),
      },
    });
    
    if (!response.ok) {
      throw new Error(`Erro ao obter projetos: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    return NextResponse.json(data);
  } catch (error) {
    console.error('Erro ao processar requisição:', error);
    return NextResponse.json(
      { error: 'Erro ao carregar projetos do usuário' },
      { status: 500 }
    );
  }
} 