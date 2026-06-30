<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Inscripcion extends Model
{
    protected $table = 'Inscripciones';
    protected $primaryKey = 'id_inscripcion';
    public $timestamps = false;

    protected $fillable = ['id_estudiante', 'id_clase', 'fecha_inscripcion', 'estado'];
    protected $appends = ['id'];

    public function getIdAttribute(): int { return $this->id_inscripcion; }

    protected function casts(): array
    {
        return ['fecha_inscripcion' => 'date:Y-m-d'];
    }

    public function estudiante(): BelongsTo
    {
        return $this->belongsTo(Estudiante::class, 'id_estudiante', 'id_estudiante');
    }

    public function clase(): BelongsTo
    {
        return $this->belongsTo(Clase::class, 'id_clase', 'id_clase');
    }

    public function pagos(): HasMany
    {
        return $this->hasMany(Pago::class, 'id_inscripcion', 'id_inscripcion');
    }

    public function asistencias(): HasMany
    {
        return $this->hasMany(Asistencia::class, 'id_inscripcion', 'id_inscripcion');
    }
}
