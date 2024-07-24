from flask import Flask, request, render_template
import pymssql

app = Flask(__name__)

# querys qu armazenei
queries = { 
    'procedure': """SELECT 
NAME AS PROCEDURE_NAME,
create_date AS CREATION_DATE,
'Active' AS STATUS 
FROM sys.procedures
WHERE UPPER(name) NOT IN (
'ATUALIZA_ALOC',
'CORRIGE_NUMERO_PARCELA_MIGRADA',
'CORRIGE_STATUS_ACORDO_MIGRADO',
'DROP_FOREIGNKEY',
'dt_addtosourcecontrol',
'dt_addtosourcecontrol_u',
'dt_adduserobject',
'dt_adduserobject_vcs',
'dt_checkinobject',
'dt_checkinobject_u',
'dt_checkoutobject',
'dt_checkoutobject_u',
'dt_displayoaerror',
'dt_displayoaerror_u',
'dt_droppropertiesbyid',
'dt_dropuserobjectbyid',
'dt_generateansiname',
'dt_getobjwithprop',
'dt_getobjwithprop_u',
'dt_getpropertiesbyid',
'dt_getpropertiesbyid_u',
'dt_getpropertiesbyid_vcs',
'dt_getpropertiesbyid_vcs_u',
'dt_isundersourcecontrol',
'dt_isundersourcecontrol_u',
'dt_removefromsourcecontrol',
'dt_setpropertybyid',
'dt_setpropertybyid_u',
'dt_validateloginparams',
'dt_validateloginparams_u',
'dt_vcsenabled',
'dt_verstamp006',
'dt_whocheckedout',
'dt_whocheckedout_u',
'INS_UP_PESSOA',
'INS_UP_PROCESSO',
'P_ATUALIZAR_ATIVIDADE',
'P_INSERE_CLASSE_PES',
'P_INSERIR_ATIVIDADE',
'PROC_ATUALIZA_VALORES_PROCESSO',
'sp_atu_dt_fatura',
'sp_corrige_outras_classes_pes',
'sp_corrige_sequence',
'SP_Insere_Fatura_Imposto',
'sp_popula_area',
'sp_popula_area_acao',
'sp_popula_area_andam',
'sp_popula_area_descricao',
'sp_popula_area_fase',
'sp_popula_area_foro',
'sp_popula_area_foro_total',
'sp_popula_area_garantia',
'sp_popula_area_indice',
'sp_popula_area_materia',
'sp_popula_area_risco',
'sp_popula_area_rito',
'sp_popula_area_subdiv',
'SP_RETURN_PROC_VALOR',
'sp_tarefa_adm',
'TH_SEQUENCE',
'sp_upgraddiagrams',
'sp_helpdiagrams',
'sp_helpdiagramdefinition',
'sp_creatediagram',
'sp_renamediagram',
'sp_alterdiagram',
'sp_dropdiagram');""",

    'trigger': """SELECT 
trg.NAME AS trigger_name,
tbl.name AS table_name,
trg.create_date AS creation_date,
CASE 
WHEN trg.is_disabled = 0 
THEN 'Active'
ELSE 'Inactive' 
END AS status
FROM SYS.triggers trg
INNER JOIN SYS.tables tbl ON trg.parent_id = tbl.object_id
WHERE trg.is_disabled = 0
AND UPPER(trg.NAME) NOT IN (
'TG_INSUP_PROCESSO_DT_INI_ENCER',
'DESDOBRAMENTO_AU_ANDAM',
'INSTANCIA_BD0',
'PROCESSO_PROC_FASE',
'TG_INS_ANDAM_PESSOA_ATIVIDADE',
'SARBOX_GARANTIA_BUD',
'LANCAMENTO_LIVRO_CAIXA_ATU_REF',
'TITULO_ATU_REF',
'ALOCACAO_BU_FAT',
'TG_UPD_ANDAM_PESSOA_ATIVIDADE',
'ALOCACAO_ATU_REF',
'DEL_PROCESSO_VISAO',
'ANDAMENTO_PROCESSO',
'ANDAMENTO_CLIENTE',
'TGR_ARQPASTA_PROCESSO_AU',
'TGR_ARQPASTA_UNIDADE_AU',
'ALOCACAO_PROCESSO',
'ALOCACAO_CLIENTE',
'TG_DEL_ANDAM_PESSOA_ATIVIDADE',
'TG_DEL_CLASSE_PESSOA',
'DESPESA_CLIENTE',
'DESPESA_PROCESSO',
'DOCUMENTO_PROCESSO',
'TG_DEL_DOMINIO',
'HONORARIO_PROCESSO',
'HONORARIO_CLIENTE',
'TG_DEL_INSTANCIA',
'PROCESSO_UP_DOMINIOS',
'PROC_JURIS_PROCESSO',
'PROC_PESSOA_CLASSE_PES',
'ANDAMENTO_AU_ATIVIDADE',
'AI_CLASSE_ACESSO_MENU',
'SARBOX_PROC_VALOR_BUD',
'BIU_HIST_PROC_GARANTIA_SARBOX');"""
}

@app.route('/')
def conversor_query():
    return render_template('conversor.html')

# Função para estabelecer conexão com o banco de dados por preenchimento
def get_db_connection(servidor, user, passwd, database):
    conn = pymssql.connect(server=servidor,
                           user=user,
                           password=passwd,
                           database=database)
    return conn


@app.route('/submit_query', methods=['POST'])
def submit_query():
    results = []
    query = request.form.get('query')
    servidor = request.form.get('servidor')
    user = request.form.get('user')
    passwd = request.form.get('passwd')
    database = request.form.get('database')
  
    if query and query in queries and servidor and user and passwd and database:
        try:
            conn = get_db_connection(servidor, user, passwd, database)
            cursor = conn.cursor(as_dict=True)
            
            # Execute a consulta SQL correspondente ao termo de busca
            sql_query = queries[query]
            print(f"Executing SQL Query: {sql_query}")  # Debug: Print SQL query
            cursor.execute(sql_query)
            
            results = cursor.fetchall()
            conn.close()
            
            print(f"Results: {results}")  # Debug: Print results
        except Exception as e:
            print(f"Error: {e}")  # Debug: Print any errors

    return render_template('resultado.html', results=results)
if __name__ == '__main__':
    app.run(debug=True)
