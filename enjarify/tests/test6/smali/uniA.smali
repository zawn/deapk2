# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
.class public Lﬃ;
.super Ljava/util/Stack;

.method public constructor <init>()V
    .locals 0
    invoke-direct {p0}, Ljava/util/Stack;-><init>()V
    return-void
.end method

.method public size()F
    .locals 0
    invoke-super {p0}, Ljava/util/Stack;->size()I
    move-result p0
    int-to-float p0, p0
    return p0
.end method