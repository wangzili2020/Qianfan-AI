import pygame
import os
import langqian
import qianfan
os.environ["QIANFAN_AK"] = ""
os.environ["QIANFAN_SK"] = ""

# 提示词的模板
from langchain import PromptTemplate
# 引入百度千帆平台的大语言模型
from langchain.llms.baidu_qianfan_endpoint import QianfanLLMEndpoint

class MyFrame:
    def __init__(self):
        # 初始化pygame
        pygame.init()

        # 设置窗口大小
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # 创建输入框和按钮
        self.text_input = pygame.Rect(10, 10, 200, 30)
        self.button = pygame.Rect(10, 50, 100, 30)

        # 初始化输入框文本
        self.text_input_text = ""

    def on_button_click(self):
        # 调用处理函数处理输入框的内容并显示结果
        result = self.process_input(self.text_input_text)
        pygame.display.set_caption(result)

    def process_input(self, input_text):
        llm = QianfanLLMEndpoint(model="Qianfan-Chinese-Llama-2-7B")
        # 输入提示词，要告诉大模型你的身份是什么，要做什么事情{Query}。
        template = "你作为一个经验丰富的技术人员，请为用户的问题提供解答:{Query}"
        prompt = PromptTemplate(
            input_variables=["Query"],
            template=template,
        )
        # 真实的用户输入，将其插入到提示词模版里面去
        final_prompt = prompt.format(Query=input_text)
        response = llm(final_prompt)
        result = "Hello, " + response
        return result

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button.collidepoint(event.pos):
                        self.on_button_click()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.on_button_click()
                    elif event.key == pygame.K_BACKSPACE:
                        self.text_input_text = self.text_input_text[:-1]
                elif event.type == pygame.TEXTINPUT:
                    self.text_input_text += event.text

            self.screen.fill((255, 255, 255))
            pygame.draw.rect(self.screen, (0, 0, 0), self.text_input, 2)
            pygame.draw.rect(self.screen, (0, 0, 0), self.button, 2)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    frame = MyFrame()
    frame.run()
