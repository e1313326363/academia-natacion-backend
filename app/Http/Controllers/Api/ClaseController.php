<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreClaseRequest;
use App\Models\Clase;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class ClaseController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $query = Clase::with('nivel', 'instructor');

        if ($request->filled('id_nivel')) {
            $query->where('id_nivel', $request->id_nivel);
        }
        if ($request->filled('id_instructor')) {
            $query->where('id_instructor', $request->id_instructor);
        }

        $perPage = min((int) $request->get('per_page', 15), 500);
        return response()->json($query->orderBy('nombre_clase')->paginate($perPage));
    }

    public function store(StoreClaseRequest $request): JsonResponse
    {
        $clase = Clase::create($request->validated());
        return response()->json($clase->load('nivel', 'instructor'), 201);
    }

    public function show(string $id): JsonResponse
    {
        return response()->json(Clase::with('nivel', 'instructor', 'inscripciones.estudiante')->findOrFail($id));
    }

    public function update(StoreClaseRequest $request, string $id): JsonResponse
    {
        $clase = Clase::findOrFail($id);
        $clase->update($request->validated());
        return response()->json($clase->load('nivel', 'instructor'));
    }

    public function destroy(string $id): JsonResponse
    {
        Clase::findOrFail($id)->delete();
        return response()->json(['message' => 'Clase eliminada correctamente.']);
    }
}
