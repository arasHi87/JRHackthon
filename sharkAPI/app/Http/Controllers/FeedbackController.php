<?php

namespace App\Http\Controllers;

use App\Models\Store;
use App\Models\Feedback;
use Illuminate\Http\Request;
use Faker\Factory as Faker;

class FeedbackController extends Controller
{
    public function generate()
    {
        $stores = Store::get(['id']);
        $faker = Faker::create();

        foreach ($stores as $store) {
            $id = $store->id;

            for ($x = 0; $x <= rand(3, 6); $x++) {
                Feedback::create([
                    'username' => $faker->name,
                    'store_id' => $id,
                    'rating' => rand(0, 5),
                    'comment' => $faker->text
                ]);
            }
        }

        return response()->json([], 200);
    }
}
