
# TestSprite AI Testing Report(MCP)

---

## 1️⃣ Document Metadata
- **Project Name:** backend
- **Date:** 2026-06-30
- **Prepared by:** TestSprite AI Team

---

## 2️⃣ Requirement Validation Summary

#### Test TC001 POST /api/login with valid credentials returns token
- **Test Code:** [TC001_POST_apilogin_with_valid_credentials_returns_token.py](./TC001_POST_apilogin_with_valid_credentials_returns_token.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/ff429bc4-4b76-459c-a3b6-ac23946e949f
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC002 POST /api/login with invalid credentials returns 401
- **Test Code:** [TC002_POST_apilogin_with_invalid_credentials_returns_401.py](./TC002_POST_apilogin_with_invalid_credentials_returns_401.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/0821921a-1970-4ac4-9c9e-41c5a3c49823
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC003 GET /api/me returns authenticated user
- **Test Code:** [TC003_GET_apime_returns_authenticated_user.py](./TC003_GET_apime_returns_authenticated_user.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/f5a5256c-e770-4497-b9a5-53a6014920ba
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC004 GET /api/dashboard/stats returns counts
- **Test Code:** [TC004_GET_apidashboardstats_returns_counts.py](./TC004_GET_apidashboardstats_returns_counts.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/15f867f2-c360-4a68-842f-75ebec5564ae
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC005 GET /api/estudiantes returns paginated list
- **Test Code:** [TC005_GET_apiestudiantes_returns_paginated_list.py](./TC005_GET_apiestudiantes_returns_paginated_list.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/a0fcdaec-549b-4d1a-8c32-7c07e60068ca
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC006 POST /api/estudiantes creates a student
- **Test Code:** [TC006_POST_apiestudiantes_creates_a_student.py](./TC006_POST_apiestudiantes_creates_a_student.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/3b422138-a73e-42c1-9ec6-1e99079717f0
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC007 PUT /api/estudiantes/{id} updates a student
- **Test Code:** [TC007_PUT_apiestudiantesid_updates_a_student.py](./TC007_PUT_apiestudiantesid_updates_a_student.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/29fcba76-756d-404c-8bed-6fbe569863e4
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC008 DELETE /api/estudiantes/{id} deletes student with cascade
- **Test Code:** [TC008_DELETE_apiestudiantesid_deletes_student_with_cascade.py](./TC008_DELETE_apiestudiantesid_deletes_student_with_cascade.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/4c1d4926-a60c-433d-aad9-10634d3673ad
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC009 POST /api/estudiantes with missing nombre returns 422
- **Test Code:** [TC009_POST_apiestudiantes_with_missing_nombre_returns_422.py](./TC009_POST_apiestudiantes_with_missing_nombre_returns_422.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/9c7d09fd-9a75-4064-a35f-1067324f2364
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC010 GET /api/instructores returns paginated list
- **Test Code:** [TC010_GET_apiinstructores_returns_paginated_list.py](./TC010_GET_apiinstructores_returns_paginated_list.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/37df62dc-d5ef-4de1-b09f-7592e96932ae
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC011 POST /api/instructores creates an instructor
- **Test Code:** [TC011_POST_apiinstructores_creates_an_instructor.py](./TC011_POST_apiinstructores_creates_an_instructor.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/c1eb2c6c-1039-43eb-9670-92988bfe0ef4
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC012 PUT /api/instructores/{id} updates an instructor
- **Test Code:** [TC012_PUT_apiinstructoresid_updates_an_instructor.py](./TC012_PUT_apiinstructoresid_updates_an_instructor.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/ef8b9599-505c-46d7-a2fe-5cc9ece79955
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC013 GET /api/niveles returns array of levels
- **Test Code:** [TC013_GET_apiniveles_returns_array_of_levels.py](./TC013_GET_apiniveles_returns_array_of_levels.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/5ead4cfe-5d38-4caf-9dce-52bc4bef4390
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC014 GET /api/clases returns paginated list with nivel and instructor
- **Test Code:** [TC014_GET_apiclases_returns_paginated_list_with_nivel_and_instructor.py](./TC014_GET_apiclases_returns_paginated_list_with_nivel_and_instructor.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/9ee285ea-161e-4193-8747-547faf75edb6
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC015 POST /api/clases creates a class
- **Test Code:** [TC015_POST_apiclases_creates_a_class.py](./TC015_POST_apiclases_creates_a_class.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/7f53a09a-d0e6-4957-8678-20f595cf7d5c
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC016 POST /api/clases with invalid cupo returns 422
- **Test Code:** [TC016_POST_apiclases_with_invalid_cupo_returns_422.py](./TC016_POST_apiclases_with_invalid_cupo_returns_422.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/0540b083-b6df-45dc-a1e1-c06f60801b0a
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC017 GET /api/inscripciones returns paginated list with estudiante and clase
- **Test Code:** [TC017_GET_apiinscripciones_returns_paginated_list_with_estudiante_and_clase.py](./TC017_GET_apiinscripciones_returns_paginated_list_with_estudiante_and_clase.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 2, in <module>
ModuleNotFoundError: No module named 'pytest'

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/bda6abad-adf6-495a-a657-406e4bc74f3b
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC018 POST /api/inscripciones creates an enrollment
- **Test Code:** [TC018_POST_apiinscripciones_creates_an_enrollment.py](./TC018_POST_apiinscripciones_creates_an_enrollment.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/ea983bcd-2935-446d-a998-1d9f8c96ff06
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC019 PUT /api/inscripciones/{id} updates enrollment estado
- **Test Code:** [TC019_PUT_apiinscripcionesid_updates_enrollment_estado.py](./TC019_PUT_apiinscripcionesid_updates_enrollment_estado.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/3b9b4787-e8db-48ba-8770-c6bc8e1dd972
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC020 GET /api/pagos returns paginated payments
- **Test Code:** [TC020_GET_apipagos_returns_paginated_payments.py](./TC020_GET_apipagos_returns_paginated_payments.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/6fda0924-e987-415f-af51-6331869c0684
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC021 POST /api/pagos creates a payment
- **Test Code:** [TC021_POST_apipagos_creates_a_payment.py](./TC021_POST_apipagos_creates_a_payment.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/5f1d1561-514d-40a0-a5ea-50b5993c82cb
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC022 GET /api/asistencias returns paginated attendance records
- **Test Code:** [TC022_GET_apiasistencias_returns_paginated_attendance_records.py](./TC022_GET_apiasistencias_returns_paginated_attendance_records.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/74884be1-36e0-441a-aaf1-ee48ca3c23c9
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC023 POST /api/asistencias creates an attendance record
- **Test Code:** [TC023_POST_apiasistencias_creates_an_attendance_record.py](./TC023_POST_apiasistencias_creates_an_attendance_record.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/2f14e7ea-6054-4e95-a1f8-4bc76fc90aa6
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC024 Unauthenticated request returns 401
- **Test Code:** [TC024_Unauthenticated_request_returns_401.py](./TC024_Unauthenticated_request_returns_401.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/787a6477-a971-4ed9-8756-109251741d4b
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC025 POST /api/logout revokes token
- **Test Code:** [TC025_POST_apilogout_revokes_token.py](./TC025_POST_apilogout_revokes_token.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/cc5cba4a-1ec9-487c-bdae-9cb36ed807f7/6f40c1e9-924a-4e3f-902c-a5dd294e0cf9
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---


## 3️⃣ Coverage & Matching Metrics

- **96.00** of tests passed

| Requirement        | Total Tests | ✅ Passed | ❌ Failed  |
|--------------------|-------------|-----------|------------|
| ...                | ...         | ...       | ...        |
---


## 4️⃣ Key Gaps / Risks
{AI_GNERATED_KET_GAPS_AND_RISKS}
---