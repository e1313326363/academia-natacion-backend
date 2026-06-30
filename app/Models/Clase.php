<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Clase extends Model
{
    protected $table = 'Clases';
    protected $primaryKey = 'id_clase';
    public $timestamps = false;

    protected $fillable = ['nombre_clase', 'id_nivel', 'id_instructor', 'cupo'];
    protected $appends = ['id'];

    public function getIdAttribute(): int { return $this->id_clase; }

    public function nivel(): BelongsTo
    {
        return $this->belongsTo(Nivel::class, 'id_nivel', 'id_nivel');
    }

    public function instructor(): BelongsTo
    {
        return $this->belongsTo(Instructor::class, 'id_instructor', 'id_instructor');
    }

    public function inscripciones(): HasMany
    {
        return $this->hasMany(Inscripcion::class, 'id_clase', 'id_clase');
    }
}
