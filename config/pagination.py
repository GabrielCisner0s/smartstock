from rest_framework.pagination import PageNumberPagination

#este archivo contiene la clase de paginacion para los productos y categorias
class StandardResultsSetPagination(
    PageNumberPagination
):

    page_size = 10# tamaño de página predeterminado

    page_size_query_param = "page_size"# permite a los clientes especificar el tamaño de página en la solicitud

    max_page_size = 100# tamaño máximo de página permitido

    page_query_param = "page"