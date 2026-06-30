<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateInstructorRequest extends FormRequest
{
    public function authorize(): bool { return true; }

    public function rules(): array
    {
        $id = $this->route('instructor');
        return [
            'nombre'       => ['required', 'string', 'max:80'],
            'especialidad' => ['nullable', 'string', 'max:100'],
            'email'        => ['nullable', 'email', 'max:120'],
        ];
    }
}
