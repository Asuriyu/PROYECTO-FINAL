import pytest
import io
from src.services.request import SyliusRequest
from src.routes.administrators_endpoint import AdministratorsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.administrators.schema_assertion import AssertionAdministrators
from src.assertions.administrators.error_assertion import AssertionAdministratorsError
from src.assertions.administrators.view_content_assertion import AssertionAdministratorsContent
from src.resources.payloads.administrators_payload import AdministratorsPayload
from src.data.administrators import generate_admin_data

# TC-149: Admin > Administrators > Avatar Images – Validar error al subir imagen de avatar sin token de autenticación
def test_TC149_Error_subir_avatar_sin_token():
    url = AdministratorsEndpoint.avatar_upload(admin_id="123")
    files = {"file": ("avatar.png", b"fakeimagebytes", "image/png")}
    response = SyliusRequest.post(url, headers={}, files=files)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_authentication_error(response.json())

# TC-150: Admin > Administrators > Avatar Images – Validar error al subir imagen de avatar con token inválido
def test_TC150_Error_subir_avatar_token_invalido():
    url = AdministratorsEndpoint.avatar_upload(admin_id="123")
    headers = {"Authorization": "Bearer invalid_token"}
    files = {"file": ("avatar.png", b"fakeimagebytes", "image/png")}
    response = SyliusRequest.post(url, headers, files=files)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_authentication_error(response.json())

# TC-151: Admin > Administrators > Avatar Images – Verificar error al crear avatar sin enviar archivo
def test_TC151_Error_sin_archivo(auth_headers, admin_id):
    url = AdministratorsEndpoint.avatar_upload(admin_id)
    response = SyliusRequest.post(url, auth_headers, files={})
    AssertionStatusCode.assert_status_code_400(response)
    AssertionAdministratorsError.assert_missing_file_error(response.json())

# TC-152: Admin > Administrators > Avatar Images – Verificar tamaño máximo de archivo permitido
def test_TC152_Error_tamano_maximo_archivo(auth_headers, admin_id, large_image_file):
    url = AdministratorsEndpoint.avatar_upload(admin_id)
    files = {"file": ("huge_avatar.png", large_image_file, "image/png")}
    response = SyliusRequest.post(url, auth_headers, files=files)
    AssertionStatusCode.assert_status_code_400(response)
    AssertionAdministratorsError.assert_file_size_limit_error(response.json())

# TC-153: Admin > Administrators > Avatar Images – Validar reemplazo de avatar existente
def test_TC153_Reemplazar_avatar_existente(auth_headers, admin_id, sample_avatar_file):
    url = AdministratorsEndpoint.avatar_upload(admin_id)
    SyliusRequest.post(url, auth_headers, files=sample_avatar_file)
    new_files = {"file": ("new_avatar.png", b"newfakebytes", "image/png")}
    response = SyliusRequest.post(url, auth_headers, files=new_files)
    AssertionStatusCode.assert_status_code_200_or_201(response)
    response_json = response.json()
    AssertionAdministrators.assert_avatar_upload_schema(response_json)
    AssertionAdministratorsContent.assert_avatar_replaced(response_json)

# TC-154: Admin > Administrators > Avatar Images – Validar que path devuelva URL válida
def test_TC154_Valdiar_url_valida_avatar(auth_headers, admin_id, sample_avatar_file):
    url = AdministratorsEndpoint.avatar_upload(admin_id)
    response = SyliusRequest.post(url, auth_headers, files=sample_avatar_file)
    AssertionStatusCode.assert_status_code_200_or_201(response)
    response_json = response.json()
    AssertionAdministrators.assert_avatar_upload_schema(response_json)
    AssertionAdministratorsContent.assert_valid_avatar_url(response_json["path"])

# TC-155: Admin > Administrators > Avatar Images – Validar que no se pueda subir más de un archivo a la vez
def test_TC155_Validar_que_no_se_pueda_subir_mas_de_un_archivo_a_la_vez(auth_headers, admin_id):
    url = AdministratorsEndpoint.avatar_upload(admin_id)
    files = {
        "file1": ("avatar1.png", b"fake1", "image/png"),
        "file2": ("avatar2.png", b"fake2", "image/png"),
    }
    response = SyliusRequest.post(url, auth_headers, files=files)
    AssertionStatusCode.assert_status_code_400(response)
    AssertionAdministratorsError.assert_multiple_files_error(response.json())

# TC-157: Admin > Administrators > Avatar Images – Verificar tamaño mínimo de archivo permitido
def test_TC157_Verificar_tamaño_minimo_de_archivo_permitido(auth_headers, admin_id, tiny_image_file):
    url = AdministratorsEndpoint.avatar_upload(admin_id)
    files = {"file": ("tiny.png", tiny_image_file, "image/png")}
    response = SyliusRequest.post(url, auth_headers, files=files)
    AssertionStatusCode.assert_status_code_400(response)
    AssertionAdministratorsError.assert_file_too_small_error(response.json())

# TC-158: Admin > Administrators > Avatar Images – Subir archivo de tipo imagen con extensión jpeg
# TC-159: Admin > Administrators > Avatar Images – Subir archivo de tipo imagen con extensión png
# TC-160: Admin > Administrators > Avatar Images – Subir archivo de tipo imagen con extensión jpg
# TC-161: Admin > Administrators > Avatar Images – Subir archivo de tipo imagen con extensión gif
# TC-162: Admin > Administrators > Avatar Images – Subir archivo de tipo imagen con extensión svg
@pytest.mark.parametrize("filename, mime_type, expected_status", [
    ("avatar.jpeg", "image/jpeg", 201),
    ("avatar.png", "image/png", 201),
    ("avatar.jpg", "image/jpeg", 201),
    ("avatar.gif", "image/gif", 201),
    ("avatar.svg", "image/svg+xml", 201)
])
def test_TC_Admin_AvatarImage_extensiones_validas(auth_headers, admin_id, filename, mime_type, expected_status):
    url = AdministratorsEndpoint.avatar_upload(admin_id)
    file_bytes = io.BytesIO(b"fakeimagebytes")
    files = {"file": (filename, file_bytes, mime_type)}
    response = SyliusRequest.post(url, auth_headers, files=files)
    AssertionStatusCode.assert_status_code(response, expected_status)

# TC-163: Admin > Administrators > Avatar Images – Subir archivo de imagen con un peso mínimo de 1 KB
# TC-164: Admin > Administrators > Avatar Images – Subir archivo de imagen con un peso máximo de 2 MB
# TC-169: Admin > Administrators > Avatar Images – Validar error al subir archivo de imagen con un peso por encima de 2 MB
@pytest.mark.parametrize("description, file_size_kb, expected_status", [
    ("mínimo permitido (1 KB)", 1, 201),
    ("máximo permitido (2048 KB / 2 MB)", 2048, 201),
    ("por encima del máximo (2049 KB)", 2049, 400)
])
def test_TC_Admin_AvatarImage_validar_pesos(auth_headers, admin_id, description, file_size_kb, expected_status):
    url = AdministratorsEndpoint.avatar_upload(admin_id)
    file_bytes = io.BytesIO(b"a" * (file_size_kb * 1024))
    files = {"file": ("avatar.png", file_bytes, "image/png")}
    response = SyliusRequest.post(url, auth_headers, files=files)
    AssertionStatusCode.assert_status_code(response, expected_status)

# TC-165: Admin > Administrators > Avatar Images – Validar error al subir archivo con extensión csv
# TC-166: Admin > Administrators > Avatar Images – Validar error al subir archivo con extensión xlsx
# TC-167: Admin > Administrators > Avatar Images – Validar error al subir archivo con extensión docx
# TC-168: Admin > Administrators > Avatar Images – Validar error al subir archivo con extensión pdf
@pytest.mark.parametrize("filename, mime_type, expected_status", [
    ("archivo.csv", "text/csv", 400),
    ("archivo.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 400),
    ("archivo.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 400),
    ("archivo.pdf", "application/pdf", 400)
])
def test_TC_Admin_AvatarImage_extensiones_invalidas(auth_headers, admin_id, filename, mime_type, expected_status):
    url = AdministratorsEndpoint.avatar_upload(admin_id)
    file_bytes = io.BytesIO(b"fakebytes")
    files = {"file": (filename, file_bytes, mime_type)}
    response = SyliusRequest.post(url, auth_headers, files=files)
    AssertionStatusCode.assert_status_code(response, expected_status)

# TC-170: Admin > Administrators > Avatar Images – Ingresar ID igual a 12345
# TC-171: Admin > Administrators > Avatar Images – Validar error al ingresar ID igual a 0
# TC-172: Admin > Administrators > Avatar Images – Validar error al ingresar ID string igual a “uno”
# TC-173: Admin > Administrators > Avatar Images – Validar error al ingresar ID negativo igual a -1
# TC-174: Admin > Administrators > Avatar Images – Validar error al ingresar ID decimal igual a 1.5
@pytest.mark.parametrize("admin_id, expected_status", [
    (12345, 404),
    (0, 404),
    ("uno", 404),
    (-1, 404),
    (1.5, 404)
])
def test_TC_Admin_AvatarImage_validar_parametros_ID(auth_headers, admin_id, expected_status):
    url = AdministratorsEndpoint.avatar_upload(admin_id)
    file_bytes = io.BytesIO(b"fakeimagebytes")
    files = {"file": ("avatar.png", file_bytes, "image/png")}
    response = SyliusRequest.post(url, auth_headers, files=files)
    AssertionStatusCode.assert_status_code(response, expected_status)