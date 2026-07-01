<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        User::firstOrCreate(
            ['email' => 'admin@academia.com'],
            ['name' => 'Administrador', 'password' => Hash::make('admin123'), 'role' => 'admin']
        );

        $niveles = ['Principiante', 'Intermedio', 'Avanzado', 'Competencia'];
        foreach ($niveles as $n) {
            DB::table('Niveles')->insertOrIgnore(['nombre_nivel' => $n]);
        }

        $instructor = DB::table('Instructores')->where('email', 'carlos@academia.com')->first();
        if (!$instructor) {
            DB::table('Instructores')->insert([
                'nombre' => 'Carlos Rodriguez',
                'especialidad' => 'Natacion Libre',
                'email' => 'carlos@academia.com',
                'telefono' => '555-0001',
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }

        $estudiante = DB::table('Estudiantes')->where('email', 'maria@academia.com')->first();
        if (!$estudiante) {
            DB::table('Estudiantes')->insert([
                'nombre' => 'Maria Lopez',
                'fecha_nacimiento' => '2000-01-15',
                'telefono' => '555-0002',
                'email' => 'maria@academia.com',
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }
    }
}
