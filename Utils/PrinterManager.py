from numpy import ndarray


class PrinterManager:

    @staticmethod
    def custom_print(data: str):
        if data is not None:
            print(data)

    @staticmethod
    def custom_print_array(data: ndarray):
        if data is not None:
            print(data)

    @staticmethod
    def custom_print_list(data: list):
        if data is not None:
            print(data)
