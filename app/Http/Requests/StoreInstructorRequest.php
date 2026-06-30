<?php

namespace App\Http\Requests;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Foundation\Http\FormRequest;

class StoreInstructorRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool { return true; }

    public function rules(): array
    {
        return [
            'nombre'       => ['required', 'string', 'max:80'],
            'especialidad' => ['nullable', 'string', 'max:100'],
            'email'        => ['nullable', 'email', 'max:120'],
        ];
    }
}
