<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreEstudianteRequest;
use App\Http\Requests\UpdateEstudianteRequest;
use App\Models\Estudiante;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class EstudianteController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $query = Estudiante::query();

        if ($request->filled('search')) {
            $query->where('nombre', 'like', "%{$request->search}%")
                  ->orWhere('email', 'like', "%{$request->search}%");
        }

        $perPage = min((int) $request->get('per_page', 15), 500);
        return response()->json($query->orderBy('nombre')->paginate($perPage));
    }

    public function store(StoreEstudianteRequest $request): JsonResponse
    {
        $estudiante = Estudiante::create($request->validated());
        return response()->json($estudiante, 201);
    }

    public function show(string $id): JsonResponse
    {
        $estudiante = Estudiante::with('inscripciones.clase')->findOrFail($id);
        return response()->json($estudiante);
    }

    public function update(UpdateEstudianteRequest $request, string $id): JsonResponse
    {
        $estudiante = Estudiante::findOrFail($id);
        $estudiante->update($request->validated());
        return response()->json($estudiante);
    }

    public function destroy(string $id): JsonResponse
    {
        $estudiante = Estudiante::with('inscripciones.pagos', 'inscripciones.asistencias')->findOrFail($id);
        foreach ($estudiante->inscripciones as $inscripcion) {
            $inscripcion->pagos()->delete();
            $inscripcion->asistencias()->delete();
        }
        $estudiante->inscripciones()->delete();
        $estudiante->delete();
        return response()->json(['message' => 'Estudiante eliminado correctamente.']);
    }
}
