<?php

namespace App\Http\Requests;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Foundation\Http\FormRequest;

class UpdateEstudianteRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool { return true; }

    public function rules(): array
    {
        $id = $this->route('estudiante');
        return [
            'nombre'           => ['sometimes', 'required', 'string', 'max:80'],
            'fecha_nacimiento' => ['sometimes', 'required', 'date', 'before:today'],
            'telefono'         => ['nullable', 'string', 'max:20'],
            'email'            => ['nullable', 'email', 'max:120', "unique:Estudiantes,email,{$id},id_estudiante"],
        ];
    }
}
