<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Asistencia extends Model
{
    protected $table = 'Asistencia';
    protected $primaryKey = 'id_asistencia';
    public $timestamps = false;

    protected $fillable = ['id_inscripcion', 'fecha_clase', 'asistio'];
    protected $appends = ['id'];

    public function getIdAttribute(): int { return $this->id_asistencia; }

    protected function casts(): array
    {
        return ['fecha_clase' => 'date:Y-m-d'];
    }

    public function inscripcion(): BelongsTo
    {
        return $this->belongsTo(Inscripcion::class, 'id_inscripcion', 'id_inscripcion');
    }
}
