<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreInscripcionRequest;
use App\Models\Inscripcion;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class InscripcionController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $query = Inscripcion::with('estudiante', 'clase.nivel');

        if ($request->filled('estado')) {
            $query->where('estado', $request->estado);
        }
        if ($request->filled('id_clase')) {
            $query->where('id_clase', $request->id_clase);
        }

        return response()->json($query->orderByDesc('fecha_inscripcion')->paginate(15));
    }

    public function store(StoreInscripcionRequest $request): JsonResponse
    {
        $data = $request->validated();
        $data['fecha_inscripcion'] = $data['fecha_inscripcion'] ?? now()->toDateString();
        $data['estado'] = $data['estado'] ?? 'Activo';

        $inscripcion = Inscripcion::create($data);
        return response()->json($inscripcion->load('estudiante', 'clase'), 201);
    }

    public function show(string $id): JsonResponse
    {
        return response()->json(Inscripcion::with('estudiante', 'clase.nivel', 'pagos', 'asistencias')->findOrFail($id));
    }

    public function update(Request $request, string $id): JsonResponse
    {
        $inscripcion = Inscripcion::findOrFail($id);
        $request->validate(['estado' => ['required', 'in:Activo,Suspendido,Baja']]);
        $inscripcion->update($request->only('estado'));
        return response()->json($inscripcion);
    }

    public function destroy(string $id): JsonResponse
    {
        Inscripcion::findOrFail($id)->delete();
        return response()->json(['message' => 'Inscripción eliminada correctamente.']);
    }
}
