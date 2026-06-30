<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Asistencia;
use App\Models\Clase;
use App\Models\Estudiante;
use App\Models\Inscripcion;
use App\Models\Instructor;
use App\Models\Pago;
use Illuminate\Http\JsonResponse;

class DashboardController extends Controller
{
    public function stats(): JsonResponse
    {
        return response()->json([
            'estudiantes'           => Estudiante::count(),
            'instructores'          => Instructor::count(),
            'clases'                => Clase::count(),
            'inscripciones_activas' => Inscripcion::where('estado', 'Activo')->count(),
            'pagos_pendientes'      => Pago::where('estado', 'Pendiente')->count(),
            'pagos_mes'             => (float) Pago::where('estado', 'Pagado')
                                             ->whereMonth('fecha_pago', now()->month)
                                             ->sum('monto'),
            'asistencias_hoy'       => Asistencia::where('fecha_clase', now()->toDateString())
                                                 ->where('asistio', 'Si')
                                                 ->count(),
        ]);
    }
}
