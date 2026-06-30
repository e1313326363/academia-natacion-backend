import requests
import datetime

BASE_URL = "http://localhost:8000"
LOGIN_EMAIL = "admin@academia.com"
LOGIN_PASSWORD = "admin123"
TIMEOUT = 30

def test_delete_student_with_cascade():
    session = requests.Session()
    token = None
    student_id = None
    enrollment_id = None
    payment_id = None
    attendance_id = None
    class_id = None
    level_id = None
    headers = {}

    try:
        # Login to get Bearer token
        login_resp = session.post(
            f"{BASE_URL}/api/login",
            json={"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD},
            timeout=TIMEOUT,
        )
        assert login_resp.status_code == 200, "Login failed"
        token = login_resp.json().get("token")
        assert token, "No token received on login"
        headers = {"Authorization": f"Bearer {token}"}

        # Create level (required to create class)
        level_data = {"nombre_nivel": "NivelParaTestEliminar"}
        level_resp = session.post(
            f"{BASE_URL}/api/niveles",
            json=level_data,
            headers=headers,
            timeout=TIMEOUT,
        )
        assert level_resp.status_code == 201, "Failed to create nivel"
        level_id = level_resp.json()["id"]

        # Create instructor (required to create class)
        instructor_resp = session.post(
            f"{BASE_URL}/api/instructores",
            json={"nombre": "InstructorTestForDelete"},
            headers=headers,
            timeout=TIMEOUT,
        )
        assert instructor_resp.status_code == 201, "Failed to create instructor"
        instructor_id = instructor_resp.json()["id"]

        # Create class (required to create enrollment)
        class_data = {
            "nombre_clase": "ClaseTestForDelete",
            "id_nivel": level_id,
            "id_instructor": instructor_id,
            "cupo": 10,
        }
        class_resp = session.post(
            f"{BASE_URL}/api/clases",
            json=class_data,
            headers=headers,
            timeout=TIMEOUT,
        )
        assert class_resp.status_code == 201, "Failed to create class"
        class_id = class_resp.json()["id"]

        # Create student
        today = datetime.date.today()
        dob = (today.replace(year=today.year - 20)).isoformat()
        student_data = {
            "nombre": "EstudianteParaEliminar",
            "fecha_nacimiento": dob,
            "telefono": "555-1234",
            "email": "estudiante.eliminar@test.com"
        }
        student_resp = session.post(
            f"{BASE_URL}/api/estudiantes",
            json=student_data,
            headers=headers,
            timeout=TIMEOUT,
        )
        assert student_resp.status_code == 201, "Failed to create student"
        student = student_resp.json()
        student_id = student["id"]

        # Create enrollment for the student and class
        inscripcion_data = {
            "id_estudiante": student_id,
            "id_clase": class_id,
            "estado": "Activo"
        }
        inscripcion_resp = session.post(
            f"{BASE_URL}/api/inscripciones",
            json=inscripcion_data,
            headers=headers,
            timeout=TIMEOUT,
        )
        assert inscripcion_resp.status_code == 201, "Failed to create inscripcion"
        enrollment_id = inscripcion_resp.json()["id"]

        # Create payment for the enrollment
        pago_data = {
            "id_inscripcion": enrollment_id,
            "monto": 100.0,
            "metodo_pago": "Efectivo",
            "estado": "Pagado"
        }
        pago_resp = session.post(
            f"{BASE_URL}/api/pagos",
            json=pago_data,
            headers=headers,
            timeout=TIMEOUT,
        )
        assert pago_resp.status_code == 201, "Failed to create pago"
        payment_id = pago_resp.json()["id"]

        # Create attendance for the enrollment
        asistencia_data = {
            "id_inscripcion": enrollment_id,
            "fecha_clase": today.isoformat(),
            "asistio": "Si"
        }
        asistencia_resp = session.post(
            f"{BASE_URL}/api/asistencias",
            json=asistencia_data,
            headers=headers,
            timeout=TIMEOUT,
        )
        assert asistencia_resp.status_code == 201, "Failed to create asistencia"
        attendance_id = asistencia_resp.json()["id"]

        # DELETE the student (should cascade delete inscripciones, pagos and asistencias)
        delete_resp = session.delete(
            f"{BASE_URL}/api/estudiantes/{student_id}",
            headers=headers,
            timeout=TIMEOUT,
        )
        assert delete_resp.status_code == 200, f"Failed to delete student: {delete_resp.text}"
        delete_message = delete_resp.json().get("message", "")
        assert "deleted" in delete_message.lower() or "eliminado" in delete_message.lower()

        # Verify student no longer exists (GET returns 404)
        get_student_resp = session.get(
            f"{BASE_URL}/api/estudiantes/{student_id}",
            headers=headers,
            timeout=TIMEOUT,
        )
        assert get_student_resp.status_code == 404, "Student still exists after deletion"

        # Verify enrollment no longer exists (GET inscripciones filtered by student)
        inscripciones_check_resp = session.get(
            f"{BASE_URL}/api/inscripciones",
            params={"estado": "Activo", "page": 1},
            headers=headers,
            timeout=TIMEOUT,
        )
        assert inscripciones_check_resp.status_code == 200
        enrollments = inscripciones_check_resp.json().get("data", [])
        # None of the enrollments should have the deleted student
        assert all(e.get("estudiante", {}).get("id") != student_id for e in enrollments), "Enrollment still exists after student deletion"

        # Verify payments no longer exist for the deleted enrollment
        pagos_resp = session.get(
            f"{BASE_URL}/api/pagos",
            params={"page": 1},
            headers=headers,
            timeout=TIMEOUT,
        )
        assert pagos_resp.status_code == 200
        pagos = pagos_resp.json().get("data", [])
        assert all(
            pago.get("inscripcion", {}).get("estudiante", {}).get("id") != student_id for pago in pagos
        ), "Payment still exists after student deletion"

        # Verify attendance records no longer exist for the deleted enrollment
        asistencias_resp = session.get(
            f"{BASE_URL}/api/asistencias",
            params={"page": 1},
            headers=headers,
            timeout=TIMEOUT,
        )
        assert asistencias_resp.status_code == 200
        asistencias = asistencias_resp.json().get("data", [])
        assert all(
            asistencia.get("inscripcion", {}).get("estudiante", {}).get("id") != student_id for asistencia in asistencias
        ), "Attendance still exists after student deletion"

    finally:
        # Cleanup any remaining resources if exists
        if attendance_id:
            try:
                session.delete(
                    f"{BASE_URL}/api/asistencias/{attendance_id}",
                    headers=headers,
                    timeout=TIMEOUT,
                )
            except Exception:
                pass
        if payment_id:
            try:
                session.delete(
                    f"{BASE_URL}/api/pagos/{payment_id}",
                    headers=headers,
                    timeout=TIMEOUT,
                )
            except Exception:
                pass
        if enrollment_id:
            try:
                session.delete(
                    f"{BASE_URL}/api/inscripciones/{enrollment_id}",
                    headers=headers,
                    timeout=TIMEOUT,
                )
            except Exception:
                pass
        if student_id:
            try:
                session.delete(
                    f"{BASE_URL}/api/estudiantes/{student_id}",
                    headers=headers,
                    timeout=TIMEOUT,
                )
            except Exception:
                pass
        if class_id:
            try:
                session.delete(
                    f"{BASE_URL}/api/clases/{class_id}",
                    headers=headers,
                    timeout=TIMEOUT,
                )
            except Exception:
                pass
        if level_id:
            try:
                session.delete(
                    f"{BASE_URL}/api/niveles/{level_id}",
                    headers=headers,
                    timeout=TIMEOUT,
                )
            except Exception:
                pass
        if 'instructor_id' in locals():
            try:
                session.delete(
                    f"{BASE_URL}/api/instructores/{instructor_id}",
                    headers=headers,
                    timeout=TIMEOUT,
                )
            except Exception:
                pass

test_delete_student_with_cascade()