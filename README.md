# Gerenciador de Backup

Este projeto é uma aplicação de gerenciamento de backup desenvolvida em Python usando PyQt6. A aplicação permite aos usuários selecionar diferentes métodos de compressão para arquivar pastas e arquivos. A interface gráfica é projetada para ser intuitiva e fácil de usar, oferecendo suporte para vários formatos de compressão e funcionalidades adicionais. São suportados 12 métodos de compressão e de descompressão.

Observação: É necessário ter instalado no seu PC os seguintes programas: WinRAR, 7-Zip e Bandizip. Para utilizar a compressão do WinRAR é necessário ter comprado a versão paga. Pois se trata de um software proprietário.

## Visão Geral

O projeto utiliza os seguintes módulos personalizados:

- `_2_gerenciador_GUI`: Gerencia a interface gráfica do usuário.
- `_3_metodos_compressao`: Define métodos de compressão suportados.
- `_4_motores_compressao`: Implementa motores de compressão.
- `_5_paleta_cores_design`: Fornece a paleta de cores para o design da aplicação.

## Funcionalidades

- **Adicionar Pastas e Arquivos**: Permite ao usuário adicionar pastas e arquivos para backup.
- **Testar Integridade**: Verifica a integridade dos arquivos e pastas adicionados.
- **Selecionar Método de Compressão**: Escolha entre vários métodos de compressão (RAR, ZIP, 7Z, etc.).
- **Especificar Diretórios de Saída**: Define onde os arquivos comprimidos serão armazenados.
- **Limpar Entradas e Saídas**: Limpa as entradas de pastas e arquivos e as saídas de compressão.

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/fernandoncidade/Gerenciador_BackUp_PyQt6_v.0.0.2
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd Gerenciador_BackUp_PyQt6_v.0.0.2
   ```

3. Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute o script principal:

   ```bash
   python _1_GUI_backup.py
   ```

## Uso

1. **Adicionar Pastas/Arquivos**: Clique em "Adicionar Pastas" ou "Adicionar Arquivos" e selecione os itens desejados.
2. **Testar Integridade**: Clique em "Testar Integridade" para verificar os itens adicionados.
3. **Selecionar Método de Compressão**: Use o menu de configurações para escolher o método de compressão desejado.
4. **Especificar Diretórios de Saída**: Clique no botão apropriado para definir onde os arquivos comprimidos serão salvos.
5. **Limpar Entradas/Saídas**: Use os botões para limpar as entradas e saídas conforme necessário.

## Estrutura do Código

- **`InterfaceGrafica`**: Classe principal que define a interface gráfica e interage com os métodos de compressão.
- **`GerenciadorInterface`**: Módulo responsável por gerenciar a interface do usuário.
- **`MetodoCompressao`**: Define os métodos de compressão suportados e suas implementações.

## Contribuição

Se desejar contribuir para o projeto, siga as etapas abaixo:

1. Faça um fork deste repositório.
2. Crie uma nova branch (`git checkout -b minha-branch`).
3. Faça suas alterações e adicione um commit (`git commit -am 'Adicionar nova funcionalidade'`).
4. Envie suas alterações para o repositório remoto (`git push origin minha-branch`).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

INFORMAÇÕES EXTRAS A RESPEITO DAS LICENÇAS:

  7-Zip
  ~~~~~
  License for use and distribution
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  7-Zip Copyright (C) 1999-2023 Igor Pavlov.

  The licenses for files are:

    1) 7z.dll:
         - The "GNU LGPL" as main license for most of the code
         - The "GNU LGPL" with "unRAR license restriction" for some code
         - The "BSD 3-clause License" for some code
    2) All other files: the "GNU LGPL".

  Redistributions in binary form must reproduce related license information from this file.

  Note:
    You can use 7-Zip on any computer, including a computer in a commercial
    organization. You don't need to register or pay for 7-Zip.


  GNU LGPL information
  --------------------

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You can receive a copy of the GNU Lesser General Public License from
    http://www.gnu.org/




  BSD 3-clause License
  --------------------

    The "BSD 3-clause License" is used for the code in 7z.dll that implements LZFSE data decompression.
    That code was derived from the code in the "LZFSE compression library" developed by Apple Inc,
    that also uses the "BSD 3-clause License":

    ----
    Copyright (c) 2015-2016, Apple Inc. All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    1.  Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

    2.  Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer
        in the documentation and/or other materials provided with the distribution.

    3.  Neither the name of the copyright holder(s) nor the names of any contributors may be used to endorse or promote products derived
        from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    ----




  unRAR license restriction
  -------------------------

    The decompression engine for RAR archives was developed using source
    code of unRAR program.
    All copyrights to original unRAR code are owned by Alexander Roshal.

    The license for original unRAR code has the following restriction:

      The unRAR sources cannot be used to re-create the RAR compression algorithm,
      which is proprietary. Distribution of modified unRAR sources in separate form
      or as a part of other software is permitted, provided that it is clearly
      stated in the documentation and source comments that the code may
      not be used to develop a RAR (WinRAR) compatible archiver.
    
    Igor Pavlov
    ----


  Política de Licença Bandizip
  -------------------------

	Ao comprar o Bandizip, você garante o uso do produto de acordo com a seguinte política de licença.


	Licença Permanente
		A licença do Bandizip não tem data de expiração; você pode usar o produto permanentemente após a compra ser feita.


	Disponível em qualquer lugar para qualquer pessoa
		A licença do Bandizip pode ser usada em qualquer lugar, incluindo residências e empresas, para fins comerciais e não comerciais.

		Essa elegibilidade vale igualmente para a Standard Edition, que não exige a compra de uma licença.
    ----
        