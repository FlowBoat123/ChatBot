import numpy as np

# Định nghĩa hàm để tính accuracy
def compute_accuracy(model, data):
    predictions = model.predict(data['features'])
    accuracy = np.mean(predictions == data['labels'])
    return accuracy

# Định nghĩa hàm để tính precision
def compute_precision(predictions, labels):
    true_positives = np.sum((predictions == 1) & (labels == 1))
    false_positives = np.sum((predictions == 1) & (labels == 0))
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    return precision

# Định nghĩa hàm để tính F1-score
def compute_f1_score(model, data):
    predictions = model.predict(data['features'])
    precision = compute_precision(predictions, data['labels'])
    recall = compute_recall(model, data)
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return f1_score

# Định nghĩa hàm để tính recall
def compute_recall(model, data):
    predictions = model.predict(data['features'])
    true_positives = np.sum((predictions == 1) & (data['labels'] == 1))
    false_negatives = np.sum((predictions == 0) & (data['labels'] == 1))
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    return recall

# Định nghĩa hàm để ghi lại các chỉ số
def log_metrics(num_epochs, model, data):
    accuracies = []
    f1_scores = []
    recalls = []

    for epoch in range(num_epochs):
        accuracy = compute_accuracy(model, data)
        f1_score = compute_f1_score(model, data)
        recall = compute_recall(model, data)

        accuracies.append(accuracy)
        f1_scores.append(f1_score)
        recalls.append(recall)

    # Tính trung bình
    average_accuracy = np.mean(accuracies)
    average_f1_score = np.mean(f1_scores)
    average_recall = np.mean(recalls)

    # In kết quả
    print(f'Average Accuracy: {average_accuracy:.4f}')
    print(f'Average F1-score: {average_f1_score:.4f}')
    print(f'Average Recall: {average_recall:.4f}')

# Ví dụ về một mô hình đơn giản
class SimpleModel:
    def predict(self, features):
        # Dự đoán ngẫu nhiên cho ví dụ
        return np.random.randint(0, 2, size=features.shape[0])

# Tạo dữ liệu giả cho ví dụ
model = SimpleModel()
data = {
    'features': np.random.rand(100, 10),  # 100 mẫu, 10 đặc trưng
    'labels': np.random.randint(0, 2, size=100)  # Nhãn 0 hoặc 1
}

# Gọi hàm log_metrics
num_epochs = 10  # Số lượng epochs bạn muốn tính toán
log_metrics(num_epochs, model, data)