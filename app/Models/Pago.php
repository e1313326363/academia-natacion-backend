<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Pago extends Model
{
    protected $table = 'Pagos';
    protected $primaryKey = 'id_pago';
    public $timestamps = false;

    protected $fillable = ['id_inscripcion', 'monto', 'fecha_pago', 'metodo_pago', 'estado'];

    protected $appends = ['id'];

    public function getIdAttribute(): int { return $this->id_pago; }

    protected function casts(): array
    {
        return [
            'fecha_pago' => 'date:Y-m-d',
            'monto'      => 'float',
        ];
    }

    public function inscripcion(): BelongsTo
    {
        return $this->belongsTo(Inscripcion::class, 'id_inscripcion', 'id_inscripcion');
    }
}
