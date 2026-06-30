<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Nivel extends Model
{
    protected $table = 'Niveles';
    protected $primaryKey = 'id_nivel';
    public $timestamps = false;

    protected $fillable = ['nombre_nivel'];
    protected $appends = ['id'];

    public function getIdAttribute(): int { return $this->id_nivel; }

    public function clases(): HasMany
    {
        return $this->hasMany(Clase::class, 'id_nivel', 'id_nivel');
    }
}
