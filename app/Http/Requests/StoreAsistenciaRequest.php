<?php

namespace App\Http\Requests;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Foundation\Http\FormRequest;

class StoreAsistenciaRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool { return true; }

    public function rules(): array
    {
        return [
            'id_inscripcion' => ['required', 'integer', 'exists:Inscripciones,id_inscripcion'],
            'fecha_clase'    => ['required', 'date'],
            'asistio'        => ['required', 'in:Si,No'],
        ];
    }
}
