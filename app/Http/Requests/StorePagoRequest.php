<?php

namespace App\Http\Requests;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Foundation\Http\FormRequest;

class StorePagoRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool { return true; }

    public function rules(): array
    {
        return [
            'id_inscripcion' => ['required', 'integer', 'exists:Inscripciones,id_inscripcion'],
            'monto'          => ['required', 'numeric', 'min:0.01'],
            'fecha_pago'     => ['nullable', 'date'],
            'metodo_pago'    => ['required', 'in:Efectivo,Tarjeta,Transferencia'],
            'estado'         => ['nullable', 'in:Pagado,Pendiente,Vencido'],
        ];
    }
}
