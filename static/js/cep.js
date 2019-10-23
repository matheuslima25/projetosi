$(document).ready(function() {

            function limpa_formulário_cep() {
                // Limpa valores do formulário de cep.
                $("#id_end_ruao").val("");
                $("#id_end_bairro").val("");
                $("#id_end_cidade").val("");
                $("#id_end_estado").val("");
            }

            //Quando o campo cep perde o foco.
            $("#id_end_cep").blur(function() {

                //Nova variável "cep" somente com dígitos.
                var cep = $(this).val().replace(/\D/g, '');

                //Verifica se campo cep possui valor informado.
                if (cep != "") {

                    //Expressão regular para validar o CEP.
                    var validacep = /^[0-9]{8}$/;

                    //Valida o formato do CEP.
                    if(validacep.test(cep)) {

                        //Preenche os campos com "..." enquanto consulta webservice.
                        $("#id_end_rua").val("...");
                        $("#id_end_bairro").val("...");
                        $("#id_end_cidade").val("...");
                        $("#id_end_estado").val("...");

                        //Consulta o webservice viacep.com.br/
                        $.getJSON("https://viacep.com.br/ws/"+ cep +"/json/", function(dados) {

                            if (!("erro" in dados)) {
                                //Atualiza os campos com os valores da consulta.
                                $("#id_end_rua").val(dados.logradouro);
                                $("#id_end_bairro").val(dados.bairro);
                                $("#id_end_cidade").val(dados.localidade);
                                $("#id_end_estado").val(dados.uf);
                                $("#select2-idend_estado-container").html(dados.uf);
                            } //end if.
                            else {
                                //CEP pesquisado não foi encontrado.
                                limpa_formulário_cep();
                                alert("CEP não encontrado.");
                            }
                        });
                    } //end if.
                    else {
                        //cep é inválido.
                        limpa_formulário_cep();
                        alert("Formato de CEP inválido.");
                    }
                } //end if.
                else {
                    //cep sem valor, limpa formulário.
                    limpa_formulário_cep();
                }
            });
});