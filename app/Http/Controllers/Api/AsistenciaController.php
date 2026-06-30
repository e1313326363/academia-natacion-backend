<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreAsistenciaRequest;
use App\Models\Asistencia;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class AsistenciaController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $query = Asistencia::with('inscripcion.estudiante', 'inscripcion.clase');

        if ($request->filled('id_inscripcion')) {
            $query->where('id_inscripcion', $request->id_inscripcion);
        }
        if ($request->filled('fecha_clase')) {
            $query->where('fecha_clase', $request->fecha_clase);
        }

        return response()->json($query->orderByDesc('fecha_clase')->paginate(15));
    }

    public function store(StoreAsistenciaRequest $request): JsonResponse
    {
        $asistencia = Asistencia::create($request->validated());
        return response()->json($asistencia->load('inscripcion.estudiante'), 201);
    }

    public function show(string $id): JsonResponse
    {
        return response()->json(Asistencia::with('inscripcion.estudiante', 'inscripcion.clase')->findOrFail($id));
    }

    public function update(Request $request, string $id): JsonResponse
    {
        $asistencia = Asistencia::findOrFail($id);
        $request->validate(['asistio' => ['required', 'in:Si,No']]);
        $asistencia->update($request->only('asistio'));
        return response()->json($asistencia);
    }

    public function destroy(string $id): JsonResponse
    {
        Asistencia::findOrFail($id)->delete();
        return response()->json(['message' => 'Registro de asistencia eliminado.']);
    }
}
