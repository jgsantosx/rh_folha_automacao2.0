📘 README – Sistema de Automação de Folha de Pagamento (RH)
📝 Descrição do Projeto

Este projeto automatiza o processamento mensal da folha de pagamento de colaboradores.
A aplicação lê uma planilha Excel com os dados dos funcionários, realiza cálculos de salário, horas extras e descontos, e exporta automaticamente:

✔ Um Excel final consolidado

✔ Um PDF completo com resumo geral + tabela detalhada

É ideal para pequenas empresas, escritórios de RH ou uso pessoal para organização da folha.



<img width="499" height="370" alt="image" src="https://github.com/user-attachments/assets/cf980397-9dff-4514-aaab-280be7d9e80c" />




📥 Entrada Esperada (Planilha)

A planilha Excel deve conter as seguintes colunas:

Coluna Descrição
Nome Nome do colaborador
Cargo Função
Horas_Trabalhadas Total de horas no mês
Horas_Extras Quantidade de horas extras
Faltas Número de faltas
Atestados Quantidade de atestados (não usado ainda)
Valor_Hora Valor da hora para o funcionário
⚙️ Processos Realizados

O sistema calcula automaticamente:

🧮 1. Salário Base
Salario_Base = Horas_Trabalhadas × Valor_Hora_Final

⏱️ 2. Horas Extras
Valor_Hora_Extra = Valor_Hora × (1 + percentual_hora_extra)
Total_Horas_Extras = Horas_Extras × Valor_Hora_Extra

❌ 3. Descontos por Faltas
Desconto_Falt = Faltas × 8h × Valor_Hora_Final

💰 4. Salário Final
Salario_Final = Salario_Base + Total_Horas_Extras – Desconto_Falt

📤 Exportações Geradas

Ao rodar o sistema, ele cria automaticamente uma pasta:

data/output/2025_11/

Dentro dela você recebe:

relatorio_final.xlsx
relatorio_final.pdf

✔ Excel com todos os colaboradores
✔ PDF com resumo + tabela formatada

▶️ Como Executar

Instale as dependências:

pip install -r requirements.txt

Coloque a planilha dentro da pasta:

data/input/

Execute o sistema:

python -m src.main

Verifique a saída em:

data/output/AAAA_MM/

🔧 Principais Arquivos
processor.py

Realiza todos os cálculos da folha.

loader.py

Carrega a planilha Excel.

exporter.py

Gera o Excel e o PDF final.

main.py

Executa todo o fluxo:

Carrega config

Lê planilha

Processa folha

Exporta resultados

📌 Exemplo de Uso
from src.main import main

main()

📄 Requisitos

Python 3.

📝 Como remover ou adicionar colunas no sistema (Guia rápido)

Este sistema permite alterar quais colunas são usadas na planilha de entrada.
Para remover ou adicionar colunas, altere somente os arquivos do módulo Loader.

✅ 1. Editar lista de colunas obrigatórias

Arquivo: src/loader.py

Localize:

REQUIRED_COLUMNS = [
"Nome", "CPF", "Cargo", "Departamento", "Data_Admissao",
"Horas_Trabalhadas", "Horas_Extras", "Faltas",
"Atestados", "Valor_Hora", "Observacoes"
]

👉 Para remover uma coluna (ex.: Observacoes), basta apagar da lista.
👉 Para adicionar, basta colocar o nome na lista.

✅ 2. Remover conversão de tipos da coluna

Ainda no loader.py, localize a função:

def \_convert_types(self, df):

Se a coluna foi removida, apague também qualquer linha que trate dela.
Exemplo — para remover “Observacoes”, delete:

df["Observacoes"] = df["Observacoes"].astype(str)

✅ 3. Processor não precisa ser alterado

O arquivo processor.py só usa estas colunas:

Valor_Hora

Horas_Trabalhadas

Horas_Extras

Faltas

Se você remover qualquer outra coluna (ex.: Cargo, Departamento, Observacoes), o Processor continua funcionando normalmente.

✅ 4. Excel e PDF são automáticos

O Exporter usa apenas as colunas existentes no DataFrame final, então:

Se você remover uma coluna no Loader → ela some automaticamente do Excel e do PDF

Não é necessário alterar nada em exporter.py

APARECE ASSIM:


<img width="1178" height="783" alt="Captura de tela 2025-11-28 225600" src="https://github.com/user-attachments/assets/da87460b-bb08-431a-b5ba-893ea45591d2" />


📌 Resumo final

Para remover uma coluna:

Tire o nome dela de REQUIRED_COLUMNS

Remova qualquer conversão de tipo dessa coluna em \_convert_types

(Opcional) Ajuste a planilha de entrada

O PDF e o Excel se ajustam automaticamente
