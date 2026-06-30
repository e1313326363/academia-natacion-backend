<?php

namespace App\Http\Requests;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Foundation\Http\FormRequest;

class StoreClaseRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool { return true; }

    public function rules(): array
    {
        return [
            'nombre_clase'  => ['required', 'string', 'max:100'],
            'id_nivel'      => ['required', 'integer', 'exists:Niveles,id_nivel'],
            'id_instructor' => ['required', 'integer', 'exists:Instructores,id_instructor'],
            'cupo'          => ['required', 'integer', 'min:1', 'max:50'],
        ];
    }
}
