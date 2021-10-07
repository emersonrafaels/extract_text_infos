from inspect import stack

from dynaconf import settings

from UTILS.check_similarity import Check_Similarity
from  UTILS.generic_functions import drop_duplicates_list


class Extract_Infos():

    def __init__(self, json_input, text, model_matchs_result):

        # 1 - INPUT DO MODELO
        self.json_input = json_input

        # 2 - TEXTO DE ANÁLISE
        self.text = text

        # 3 - RESULTADOS DOS MATCHS
        self.model_matchs_result = model_matchs_result

        # 4 - INICIANDO O JSON DE RESULTADO FINAL
        self.result = settings.MASK_RESULT_JSON

        # 5 - INICIANDO OS PERCENTUAIS DE MATCH DEFAULT
        self.default_percent_match = settings.DEFAULT_PERCENTUAL_MATCH

        # 6 - DEFININDO SE DEVE HAVER PRÉ PROCESSAMENTO DOS ITENS ANTES DO CÁLCULO DE SEMELHANÇA
        self.similarity_pre_processing = settings.DEFAULT_PRE_PROCESSING

        # 7 - INICIANDO A VARIÁVEL QUE CONTÉM O LIMIT NA CHAMADA DE MÁXIMAS SIMILARIDADES
        self.limit_result_best_similar = settings.DEFAULT_LIMIT_RESULT_BEST_SIMILAR



    def get_values(self, data, field):

        """

            DADO UM CAMPO
            OBTÉM OS VALORES PRESENTES NO DOCUMENTO

            PARA OBTER OS VALORES, REALIZA A RECUPERAÇÃO
            DAS NFORMAÇÕES CONTIDAS NOS MATCHS JÁ OBTIDOS.

            # Arguments
                data                  - Required : Dados dos matchs (Dict)

            # Returns
                list_result           - Required : Resultado contendo a lista de valores (List)

        """

        # INICIANDO A VARIÁVEL QUE ARMAZENARÁ TODOS OS VALORES CONTIDOS NO TEXTO
        list_result = []

        try:
            list_result = [value[3] for value in data[field][0]]

            # RETIRANDO DULICIDADES DA LIST RESULT
            list_result = drop_duplicates_list(list_result)

        except Exception as ex:
            print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

        return list_result


    def decorator_valid_similarity(func):

        """

            ORQUESTRA A CHAMADA DA FUNÇÃO DE CÁLCULO DE SIMILARIDADE ITEM A ITEM.

            # Arguments
                search                     - Required : Palavra a ser comparada
                                                        ou utilizada como base para obter
                                                        as similaridades
                                                        dentre as possibilidades (String)

                list_choices               - Required : Palavra ser comparada com a query ou a lista
                                                        de palavras a serem comparadas
                                                        com a query (String | List)

                percent_match              - Required : Somente serão retornados
                                                        os itens acima do
                                                        percentual de match (Integer)

                pre_processing             - Optional : Definindo se deve haver
                                                        pré processamento (Boolean)

                limit                      - Optional : Limite de resultados
                                                        de similaridade (Integer)

            # Returns
                percentual_similarity      - Required : Percentual de similaridade (String | List)

        """

        def valid_value_similarity(self, search, list_choices, percent_match, pre_processing, limit):

            # INICIANDO A VARIÁVEL QUE ARMAZENARÁ O RESULTADO DE SIMILARIDADES
            # APÓS FILTRO POR PERCENTUAL DE MATCH ESPERADO
            result_valid_similarity = []
            validator_similarity = False

            # VALIDANDO O LIMITE ENVIADO
            if limit is False:
                limit = None

            try:
                # OBTENDO AS SIMILARIDADES ENTRE O ITEM PROCURADO E A LISTA DE ITENS
                result_similarity = Check_Similarity.get_values_similarity(query=search,
                                                                           choices=list_choices,
                                                                           pre_processing=pre_processing,
                                                                           limit=limit)

                # VALIDANDO OS ITENS QUE ESTÃO ACIMA DO PERCENTUAL DE SIMILARIDADE ENVIADO
                result_valid_similarity = [value for value in result_similarity if value[1] > percent_match]

                if len(result_valid_similarity) > 0:
                    validator_similarity = True

            except Exception as ex:
                print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

            return validator_similarity, result_valid_similarity

        return valid_value_similarity


    @decorator_valid_similarity
    def valid_values(self):

        pass


    def orchestra_infos_rules(self):

        if "todos" in self.json_input["campos_desejados"]:

            # VALIDANDO A SIMILARIDADE
            self.result["validator_name"], self.result["name"] = Extract_Infos.valid_values(self,
                                                                                            self.model_matchs_result["nome"],
                                                                                            self.model_matchs_result["todos_nomes"],
                                                                                            self.json_input["percent_match"],
                                                                                            self.similarity_pre_processing,
                                                                                            self.limit_result_best_similar)

            return self.result
