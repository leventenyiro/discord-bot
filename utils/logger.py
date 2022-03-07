from utils.promptcolor import PromptColors

class Logger:
    @staticmethod
    def progress(text):
        print(f'{PromptColors.CBLUE2}{text}{PromptColors.CEND}')

    @staticmethod
    def warning(text):
        print(f'{PromptColors.CYELLOW}{text}{PromptColors.CEND}')
    
    @staticmethod
    def success(text):
        print(f'{PromptColors.CGREEN}{text}{PromptColors.CEND}')

    @staticmethod
    def error(text):
        print(f'{PromptColors.CRED}{text}{PromptColors.CEND}')

    @staticmethod
    def info(text):
        print(f'{text}')
