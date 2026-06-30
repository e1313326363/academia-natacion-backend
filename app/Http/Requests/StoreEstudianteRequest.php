<?php

namespace App\Http\Requests;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Foundation\Http\FormRequest;

class StoreEstudianteRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool { return true; }

    public function rules(): array
    {
        return [
            'nombre'           => ['required', 'string', 'max:80'],
            'fecha_nacimiento' => ['required', 'date', 'before:today'],
            'telefono'         => ['nullable', 'string', 'max:20'],
            'email'            => ['nullable', 'email', 'max:120', 'unique:Estudiantes,email'],
        ];
    }
}
