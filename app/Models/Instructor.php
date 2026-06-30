<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Instructor extends Model
{
    protected $table = 'Instructores';
    protected $primaryKey = 'id_instructor';
    public $timestamps = false;

    protected $fillable = ['nombre', 'especialidad', 'email'];
    protected $appends = ['id'];

    public function getIdAttribute(): int { return $this->id_instructor; }

    public function clases(): HasMany
    {
        return $this->hasMany(Clase::class, 'id_instructor', 'id_instructor');
    }
}
