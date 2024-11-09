import streamlit as st
import random
import pygame
import time

# Inicializa o pygame para tocar sons
pygame.mixer.init()
som_sucesso = pygame.mixer.Sound("success.wav")  # Som de sucesso
som_erro = pygame.mixer.Sound("error.wav")        # Som de erro

# Função para gerar uma nova pergunta
def gerar_pergunta(operacao):
    numero1 = random.randint(1, 10)
    numero2 = random.randint(1, 10)
    if operacao == "multiplicacao":
        pergunta = f"Qual é {numero1} x {numero2}?"
        resposta_certa = numero1 * numero2
    elif operacao == "adicao":
        pergunta = f"Qual é {numero1} + {numero2}?"
        resposta_certa = numero1 + numero2
    elif operacao == "subtracao":
        pergunta = f"Qual é {numero1} - {numero2}?"
        resposta_certa = numero1 - numero2
    elif operacao == "divisao":
        numero1 = numero2 * random.randint(1, 10)  # Para evitar divisão por zero
        pergunta = f"Qual é {numero1} ÷ {numero2}?"
        resposta_certa = numero1 // numero2  # Divisão inteira
    return pergunta, resposta_certa

# Função para verificar a resposta do usuário
def verificar_resposta(resposta_usuario, resposta_certa):
    if resposta_usuario == resposta_certa:
        st.success("Muito bem! Você acertou!")
        som_sucesso.play()  # Toca o som de sucesso
        return True
    else:
        st.error(f"Ops! A resposta certa é {resposta_certa}. Tente novamente!")
        som_erro.play()  # Toca o som de erro
        return False

# Função principal da aplicação
def main():
    st.title("Aprendendo Matemática de Forma Divertida")

    # Inicializa as variáveis de estado
    if "pontos" not in st.session_state:
        st.session_state.pontos = 0
    if "tentativas" not in st.session_state:
        st.session_state.tentativas = 0
    if "acertos" not in st.session_state:
        st.session_state.acertos = 0
    if "erros" not in st.session_state:
        st.session_state.erros = 0
    if "mostrar_baloes" not in st.session_state:
        st.session_state.mostrar_baloes = False

    operacao = st.radio("Escolha a operação:", ["multiplicacao", "adicao", "subtracao", "divisao"])

    if "pergunta" not in st.session_state or "resposta_certa" not in st.session_state:
        st.session_state.pergunta, st.session_state.resposta_certa = gerar_pergunta(operacao)

    with st.form(key='form'):
        st.write(st.session_state.pergunta)
        resposta_usuario = st.number_input("Digite sua resposta:", step=1)
        submit_button = st.form_submit_button(label='Enviar')

        if submit_button:
            st.session_state.tentativas += 1  # Incrementa o total de tentativas
            if verificar_resposta(resposta_usuario, st.session_state.resposta_certa):
                st.session_state.pontos += 1
                st.session_state.acertos += 1  # Incrementa acertos
                st.session_state.mostrar_baloes = True  # Ativa a exibição dos balões
                time.sleep(1)  # Espera 1 segundo para que os balões apareçam
                st.session_state.pergunta, st.session_state.resposta_certa = gerar_pergunta(operacao)
                st.rerun()  # Rerun para atualizar a pergunta
            else:
                st.session_state.erros += 1  # Incrementa erros
                st.session_state.mostrar_baloes = False  # Desativa a exibição dos balões


    # Exibe as estatísticas
    st.write(f"Pontos: {st.session_state.pontos}")
    st.write(f"Tentativas: {st.session_state.tentativas}")
    st.write(f"Acertos: {st.session_state.acertos}")
    st.write(f"Erros: {st.session_state.erros}")

    if st.session_state.mostrar_baloes:
        st.balloons()  # Mostra os balões se a condição for verdadeira


if __name__ == "__main__":
    main()
