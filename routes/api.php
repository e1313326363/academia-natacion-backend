<?php

use App\Http\Controllers\Api\AsistenciaController;
use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\ClaseController;
use App\Http\Controllers\Api\DashboardController;
use App\Http\Controllers\Api\EstudianteController;
use App\Http\Controllers\Api\InscripcionController;
use App\Http\Controllers\Api\InstructorController;
use App\Http\Controllers\Api\NivelController;
use App\Http\Controllers\Api\PagoController;
use Illuminate\Support\Facades\Route;

// Rutas públicas (sin autenticación)
Route::post('/login', [AuthController::class, 'login']);

// Rutas protegidas con Sanctum
Route::middleware('auth:sanctum')->group(function () {

    // Auth
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/me', [AuthController::class, 'me']);

    // Dashboard
    Route::get('/dashboard/stats', [DashboardController::class, 'stats']);

    // CRUD recursos
    Route::apiResource('estudiantes',   EstudianteController::class);
    Route::apiResource('instructores',  InstructorController::class);
    Route::apiResource('niveles',       NivelController::class);
    Route::apiResource('clases',        ClaseController::class);
    Route::apiResource('inscripciones', InscripcionController::class);
    Route::apiResource('pagos',         PagoController::class);
    Route::apiResource('asistencias',   AsistenciaController::class);
});
