<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\StorePagoRequest;
use App\Models\Pago;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class PagoController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $query = Pago::with('inscripcion.estudiante');

        if ($request->filled('estado')) {
            $query->where('estado', $request->estado);
        }
        if ($request->filled('metodo_pago')) {
            $query->where('metodo_pago', $request->metodo_pago);
        }

        return response()->json($query->orderByDesc('fecha_pago')->paginate(15));
    }

    public function store(StorePagoRequest $request): JsonResponse
    {
        $data = $request->validated();
        $data['fecha_pago'] = $data['fecha_pago'] ?? now()->toDateString();
        $data['estado'] = $data['estado'] ?? 'Pagado';

        $pago = Pago::create($data);
        return response()->json($pago->load('inscripcion.estudiante'), 201);
    }

    public function show(string $id): JsonResponse
    {
        return response()->json(Pago::with('inscripcion.estudiante', 'inscripcion.clase')->findOrFail($id));
    }

    public function update(Request $request, string $id): JsonResponse
    {
        $pago = Pago::findOrFail($id);
        $request->validate(['estado' => ['required', 'in:Pagado,Pendiente,Vencido']]);
        $pago->update($request->only('estado'));
        return response()->json($pago);
    }

    public function destroy(string $id): JsonResponse
    {
        Pago::findOrFail($id)->delete();
        return response()->json(['message' => 'Pago eliminado correctamente.']);
    }
}
