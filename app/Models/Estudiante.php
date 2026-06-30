<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Estudiante extends Model
{
    protected $table = 'Estudiantes';
    protected $primaryKey = 'id_estudiante';
    public $timestamps = false;

    protected $fillable = ['nombre', 'fecha_nacimiento', 'telefono', 'email'];
    protected $appends = ['id'];

    public function getIdAttribute(): int { return $this->id_estudiante; }

    protected function casts(): array
    {
        return ['fecha_nacimiento' => 'date:Y-m-d'];
    }

    public function inscripciones(): HasMany
    {
        return $this->hasMany(Inscripcion::class, 'id_estudiante', 'id_estudiante');
    }
}
