CREATE TABLE IF NOT EXISTS decks (
   id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
   key uuid UNIQUE NOT NULL,
   data jsonb NOT NULL
);

CREATE TABLE IF NOT EXISTS flashcards (
   id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
   key uuid UNIQUE NOT NULL,
   data jsonb NOT NULL
);
