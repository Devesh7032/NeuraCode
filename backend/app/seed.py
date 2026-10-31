import uuid
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.user import User, Profile, UserStreak, Badge, UserBadge, UserBookmark
from app.models.challenge import Challenge, ChallengeTest, ChallengeHint
from app.models.submission import Submission, SubmissionResult
from app.models.progress import LearningPath, LearningPathItem, UserProgress
from app.models.execution import Execution

# Import challenge lists from modular folders
from app.challenges.python_for_ai import challenges as python_challenges
from app.challenges.mathematics import challenges as math_challenges
from app.challenges.machine_learning import challenges as ml_challenges
from app.challenges.deep_learning import challenges as dl_challenges
from app.challenges.computer_vision import challenges as cv_challenges
from app.challenges.nlp_transformers import challenges as nlp_challenges
from app.challenges.genai_rag import challenges as genai_challenges
from app.challenges.agents_mlops import challenges as agent_challenges

def seed_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print("Seeding/updating challenges...")

        # Combine all challenges
        all_challenges_data = (
            python_challenges +
            math_challenges +
            ml_challenges +
            dl_challenges +
            cv_challenges +
            nlp_challenges +
            genai_challenges +
            agent_challenges
        )

        vis_mappings = {
            "sigmoid-activation": ("FUNCTION", {"x_min": -10, "x_max": 10, "label": "Sigmoid"}),
            "relu-activation": ("FUNCTION", {"x_min": -10, "x_max": 10, "label": "ReLU"}),
            "tanh-activation": ("FUNCTION", {"x_min": -10, "x_max": 10, "label": "Tanh"}),
            "softmax-activation": ("BAR_CHART", {"label_x": "Class", "label_y": "Probability"}),
            "normalize-vector": ("VECTOR", {"dimensions": 2}),
            "matrix-multiplication": ("MATRIX_MULTIPLICATION", {}),
            "single-step-gradient-descent": ("GRADIENT_DESCENT", {"learning_rate_default": 0.1, "iterations_default": 20}),
            "linear-regression-prediction": ("LINEAR_REGRESSION", {}),
            "k-means-centroid": ("K_MEANS", {"k_default": 2}),
            "pca-projection": ("PCA", {}),
            "dense-layer-forward": ("DENSE_LAYER", {}),
            "nn-forward-pass": ("NEURAL_NETWORK", {"layers": [2, 2, 1]}),
            "scaled-dot-product": ("SCALED_DOT_PRODUCT", {}),
            "attention-scores": ("ATTENTION_SCORES", {}),
            "self-attention-weights": ("SELF_ATTENTION", {}),
            "embedding-similarity": ("EMBEDDING_SIMILARITY", {})
        }

        import json as json_mod
        for challenge_dict in all_challenges_data:
            # Create a shallow copy to prevent editing module arrays
            c_data = challenge_dict.copy()
            tests = c_data.pop("tests")
            hints = c_data.pop("hints")

            slug = c_data.get("slug")
            if slug in vis_mappings:
                v_type, v_conf = vis_mappings[slug]
                c_data["visualization_type"] = v_type
                c_data["visualization_config"] = json_mod.dumps(v_conf)

            # Query existing challenge by slug
            challenge = db.query(Challenge).filter_by(slug=slug).first()
            if not challenge:
                challenge = Challenge(**c_data)
                db.add(challenge)
                db.flush() # populate challenge.id
            else:
                # Update attributes
                for key, value in c_data.items():
                    setattr(challenge, key, value)
                db.flush()

            for t in tests:
                existing_test = db.query(ChallengeTest).filter_by(
                    challenge_id=challenge.id,
                    input_data=t["input_data"]
                ).first()
                if not existing_test:
                    test_case = ChallengeTest(challenge_id=challenge.id, **t)
                    db.add(test_case)
                else:
                    existing_test.expected_output = t["expected_output"]
                    existing_test.is_public = t.get("is_public", True)

            for h in hints:
                existing_hint = db.query(ChallengeHint).filter_by(
                    challenge_id=challenge.id,
                    hint_text=h["hint_text"]
                ).first()
                if not existing_hint:
                    hint = ChallengeHint(challenge_id=challenge.id, **h)
                    db.add(hint)

        print("Seeding default Learning Paths...")
        paths = [
            {
                "title": "Machine Learning Path",
                "slug": "machine-learning-path",
                "description": "Master foundational mathematics, regressions, classification metrics, and PCA dimensionality reductions.",
                "category": "Machine Learning",
                "items": [
                    {"title": "Arithmetic Mean", "slug": "mean-of-a-dataset"},
                    {"title": "Vector Dot Product", "slug": "dot-product"},
                    {"title": "Matrix Multiplication", "slug": "matrix-multiplication"},
                    {"title": "Vector Norm Normalization", "slug": "normalize-vector"},
                    {"title": "Linear Regression Prediction", "slug": "linear-regression-prediction"},
                    {"title": "Mean Squared Error", "slug": "mean-squared-error"},
                    {"title": "Logistic Regression Prediction", "slug": "logistic-prediction"},
                    {"title": "Binary Cross Entropy Loss", "slug": "binary-cross-entropy"},
                    {"title": "Classification Accuracy", "slug": "accuracy-metric"},
                    {"title": "K-Means Assignment", "slug": "k-means-centroid"},
                    {"title": "Principal Component Analysis", "slug": "pca-projection"}
                ]
            },
            {
                "title": "Deep Learning Path",
                "slug": "deep-learning-path",
                "description": "Formulate deep network layers, activation functions, losses, and backpropagation gradients.",
                "category": "Deep Learning",
                "items": [
                    {"title": "ReLU Activation", "slug": "relu-activation"},
                    {"title": "Tanh Activation", "slug": "tanh-activation"},
                    {"title": "Softmax Classification Probability", "slug": "softmax-activation"},
                    {"title": "Dense Layer Feedforward", "slug": "dense-layer-forward"},
                    {"title": "Neural Network Forward Pass", "slug": "nn-forward-pass"},
                    {"title": "Upstream Backpropagation Gradients", "slug": "backpropagation-step"}
                ]
            },
            {
                "title": "Generative AI Path",
                "slug": "generative-ai-path",
                "description": "Trace embeddings similarity, text search retrieval, document chunking, and self-attention transformers.",
                "category": "Generative AI",
                "items": [
                    {"title": "Text Jaccard Similarity", "slug": "text-similarity"},
                    {"title": "Tokens Cosine Similarity", "slug": "embedding-similarity"},
                    {"title": "Top-K Document Retrieval", "slug": "top-k-retrieval"},
                    {"title": "Document Overlap Chunking", "slug": "document-chunking"},
                    {"title": "Sinusoidal Positional Encoding", "slug": "positional-encoding"},
                    {"title": "Scaled Dot Product Attention", "slug": "scaled-dot-product"},
                    {"title": "Self Attention Project Layer", "slug": "self-attention-weights"}
                ]
            }
        ]

        for p_data in paths:
            items_data = p_data.pop("items")
            path = db.query(LearningPath).filter_by(slug=p_data["slug"]).first()
            if not path:
                path = LearningPath(**p_data)
                db.add(path)
                db.flush()
            else:
                for key, value in p_data.items():
                    setattr(path, key, value)
                db.flush()

            for idx, item in enumerate(items_data):
                challenge_obj = db.query(Challenge).filter_by(slug=item["slug"]).first()
                if challenge_obj:
                    p_item = db.query(LearningPathItem).filter_by(
                        learning_path_id=path.id,
                        challenge_id=challenge_obj.id
                    ).first()
                    if not p_item:
                        p_item = LearningPathItem(
                            learning_path_id=path.id,
                            challenge_id=challenge_obj.id,
                            title=item["title"],
                            order_index=idx
                        )
                        db.add(p_item)
                    else:
                        p_item.title = item["title"]
                        p_item.order_index = idx

        db.commit()
        print("Database seeding completed successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    if "--reset" in sys.argv:
        print("Force resetting database...")
        Base.metadata.drop_all(bind=engine)
    else:
        print("Seeding/updating database incrementally (preserving existing data)...")
    seed_db()
