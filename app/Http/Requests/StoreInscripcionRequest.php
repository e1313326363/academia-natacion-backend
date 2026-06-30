<?php

namespace App\Http\Requests;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Foundation\Http\FormRequest;

class StoreInscripcionRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool { return true; }

    public function rules(): array
    {
        return [
            'id_estudiante'    => ['required', 'integer', 'exists:Estudiantes,id_estudiante'],
            'id_clase'         => ['required', 'integer', 'exists:Clases,id_clase'],
            'fecha_inscripcion'=> ['nullable', 'date'],
            'estado'           => ['nullable', 'in:Activo,Suspendido,Baja'],
        ];
    }
}
