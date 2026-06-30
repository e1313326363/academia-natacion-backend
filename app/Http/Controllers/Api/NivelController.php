<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Nivel;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class NivelController extends Controller
{
    public function index(): JsonResponse
    {
        return response()->json(Nivel::orderBy('nombre_nivel')->get());
    }

    public function store(Request $request): JsonResponse
    {
        $request->validate(['nombre_nivel' => ['required', 'string', 'max:50', 'unique:Niveles,nombre_nivel']]);
        $nivel = Nivel::create($request->only('nombre_nivel'));
        return response()->json($nivel, 201);
    }

    public function show(string $id): JsonResponse
    {
        return response()->json(Nivel::with('clases')->findOrFail($id));
    }

    public function update(Request $request, string $id): JsonResponse
    {
        $nivel = Nivel::findOrFail($id);
        $request->validate(['nombre_nivel' => ['required', 'string', 'max:50', "unique:Niveles,nombre_nivel,{$id},id_nivel"]]);
        $nivel->update($request->only('nombre_nivel'));
        return response()->json($nivel);
    }

    public function destroy(string $id): JsonResponse
    {
        Nivel::findOrFail($id)->delete();
        return response()->json(['message' => 'Nivel eliminado correctamente.']);
    }
}
