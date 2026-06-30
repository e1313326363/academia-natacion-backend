<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreInstructorRequest;
use App\Http\Requests\UpdateInstructorRequest;
use App\Models\Instructor;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class InstructorController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $query = Instructor::query();

        if ($request->filled('search')) {
            $query->where('nombre', 'like', "%{$request->search}%");
        }

        return response()->json($query->orderBy('nombre')->paginate(15));
    }

    public function store(StoreInstructorRequest $request): JsonResponse
    {
        $instructor = Instructor::create($request->validated());
        return response()->json($instructor, 201);
    }

    public function show(string $id): JsonResponse
    {
        $instructor = Instructor::with('clases.nivel')->findOrFail($id);
        return response()->json($instructor);
    }

    public function update(UpdateInstructorRequest $request, string $id): JsonResponse
    {
        $instructor = Instructor::findOrFail($id);
        $instructor->update($request->validated());
        return response()->json($instructor);
    }

    public function destroy(string $id): JsonResponse
    {
        $instructor = Instructor::with('clases.inscripciones.pagos', 'clases.inscripciones.asistencias')->findOrFail($id);
        foreach ($instructor->clases as $clase) {
            foreach ($clase->inscripciones as $inscripcion) {
                $inscripcion->pagos()->delete();
                $inscripcion->asistencias()->delete();
            }
            $clase->inscripciones()->delete();
        }
        $instructor->clases()->delete();
        $instructor->delete();
        return response()->json(['message' => 'Instructor eliminado correctamente.']);
    }
}
